{
	description = "Django + Gunicorn + Nginx (TapsAff)";

	inputs = {
		nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.05";
		tapsaff-src = {
			url = "git+ssh://git@github.com/ColinWaddell/TapsAff-Django.git";
			flake = false;
		};
	};
	outputs = { self, nixpkgs, tapsaff-src, ... }:
	let
		system = "x86_64-linux";
		pkgs = import nixpkgs { inherit system; };
	in {
		nixosModules.tapsaff = { lib, config, pkgs, ... }:
		let
			cfg = config.services.tapsaff;

			pythonEnv = pkgs.python313.withPackages (p: with p; [
				django
				django-environ
				gunicorn
				mysqlclient
			]);

			appDir = "/var/lib/tapsaff/app";
			runDir = "/run/tapsaff";
			stateDir = "/var/lib/tapsaff";
			defaultStaticDir = "${appDir}/static";
			defaultMediaDir = "${appDir}/media";
			envFile = cfg.environmentFile;
			bind = "${cfg.listenAddress}:${toString cfg.listenPort}";

			manage = pkgs.writeShellScript "manage-tapsaff" ''
				set -euo pipefail
				cd ${appDir}
				exec ${pythonEnv}/bin/python manage.py "$@"
			'';

			bootstrap = pkgs.writeShellScript "tapsaff-bootstrap" ''
				set -euo pipefail
				cd ${appDir}
				set -a
				. ${envFile}
				set +a
				${manage} migrate --noinput
				${manage} collectstatic --noinput
			'';
		in {
			options.services.tapsaff = {
				enable = lib.mkEnableOption "TapsAff Django stack";
				domain = lib.mkOption {
					type = lib.types.str;
					default = "taps-aff.co.uk";
				};
				serverAliases = lib.mkOption {
					type = lib.types.listOf lib.types.str;
					default = [ "www.taps-aff.co.uk" "api.taps-aff.co.uk" "demo.taps-aff.co.uk" ];
					description = "Additional hostnames for the TapsAff nginx vhost.";
				};
				environmentFile = lib.mkOption {
					type = lib.types.path;
					default = "/var/lib/tapsaff/.env";
				};
				listenAddress = lib.mkOption {
					type = lib.types.str;
					default = "127.0.0.1";
				};
				listenPort = lib.mkOption {
					type = lib.types.port;
					default = 8001;
				};
				wsgiModule = lib.mkOption {
					type = lib.types.str;
					default = "tapsaff.wsgi:application";
				};
				workers = lib.mkOption {
					type = lib.types.int;
					default = 3;
				};
				staticRoot = lib.mkOption {
					type = lib.types.str;
					default = defaultStaticDir;
					description = "Directory served by Nginx at /static/.";
				};
				serveStaticWithNginx = lib.mkOption {
					type = lib.types.bool;
					default = true;
				};
				mediaRoot = lib.mkOption {
					type = lib.types.str;
					default = defaultMediaDir;
					description = "Directory served by Nginx at /media/.";
				};
				serveMediaWithNginx = lib.mkOption {
					type = lib.types.bool;
					default = true;
					description = "Serve MEDIA files via Nginx at /media/.";
				};
				redisPort = lib.mkOption {
					type = lib.types.port;
					default = 6380;
					description = "Port for the TapsAff Redis cache instance.";
				};
			};

			config = lib.mkIf cfg.enable {
				nix.settings.experimental-features = [ "nix-command" "flakes" ];

				users.groups.tapsaffsvc = { };
				users.users.tapsaffsvc = {
					isSystemUser = true;
					group = "tapsaffsvc";
					home = stateDir;
					description = "TapsAff Django runtime user";
				};

				systemd.tmpfiles.rules = [
					"d ${stateDir}        0750 tapsaffsvc tapsaffsvc - -"
					"d ${appDir}          0750 tapsaffsvc tapsaffsvc - -"
					"d ${runDir}          0755 tapsaffsvc tapsaffsvc - -"
					"d ${cfg.staticRoot}  0755 tapsaffsvc tapsaffsvc - -"
					"d ${cfg.mediaRoot}   0755 tapsaffsvc tapsaffsvc - -"
					"f ${stateDir}/.env   0640 tapsaffsvc tapsaffsvc - -"
				];

				system.activationScripts.tapsaff-sync.text = ''
					echo "Syncing TapsAff source into ${appDir}"
					mkdir -p ${appDir}
					chown tapsaffsvc:tapsaffsvc ${appDir}
					rm -rf ${appDir:?}/*
					cp -aT ${tapsaff-src} ${appDir}
					chown -R tapsaffsvc:tapsaffsvc ${appDir}
				'';

				systemd.targets.tapsaff = {
					description = "TapsAff Django stack";
					wantedBy = [ "multi-user.target" ];
				};

				services.redis.servers."tapsaff" = {
					enable = true;
					port = cfg.redisPort;
				};

				systemd.services.tapsaff-bootstrap = {
					description = "TapsAff DB migrate + collectstatic";
					after = [ "network-online.target" "redis-tapsaff.service" ];
					wants = [ "network-online.target" "redis-tapsaff.service" ];
					wantedBy = [ "multi-user.target" ];
					environment = { PYTHONPATH = appDir; };
					restartTriggers = [ tapsaff-src ];
					serviceConfig = {
						Type = "oneshot";
						User = "tapsaffsvc";
						Group = "tapsaffsvc";
						WorkingDirectory = appDir;
						ExecStart = "${bootstrap}";
						RemainAfterExit = true;
						EnvironmentFile = envFile;
					};
				};

				systemd.services.tapsaff-gunicorn = {
					description = "TapsAff Django via Gunicorn";
					after = [ "network.target" "tapsaff-bootstrap.service" "redis-tapsaff.service" ];
					requires = [ "tapsaff-bootstrap.service" "redis-tapsaff.service" ];
					wantedBy = [ "tapsaff.target" ];
					environment = { PYTHONPATH = appDir; };
					serviceConfig = {
						EnvironmentFile = envFile;
						User = "tapsaffsvc";
						Group = "tapsaffsvc";
						WorkingDirectory = appDir;
						RuntimeDirectory = "tapsaff";
						ExecStart = ''
							${pythonEnv}/bin/gunicorn \
								--workers ${toString cfg.workers} \
								--bind ${bind} \
								--chdir ${appDir} \
								${cfg.wsgiModule}
						'';
						Restart = "always";
					};
				};

				services.nginx = {
					enable = true;
					virtualHosts = {
						"${cfg.domain}" = {
							enableACME = true;
							forceSSL = true;
							serverAliases = cfg.serverAliases;

							locations = lib.mkMerge [
								{
									"/" = {
										proxyPass = "http://${cfg.listenAddress}:${toString cfg.listenPort}";
									};
								}

								(lib.mkIf cfg.serveStaticWithNginx {
									"/static/" = {
										alias = "${cfg.staticRoot}/";
										extraConfig = ''
											access_log off;
											expires 7d;
										'';
									};
								})

								(lib.mkIf cfg.serveMediaWithNginx {
									"/media/" = {
										alias = "${cfg.mediaRoot}/";
										extraConfig = ''
											access_log off;
											expires 0;
										'';
									};
								})
							];
						};
					};
				};

				security.acme = {
					acceptTerms = true;
					defaults.email = "example@email.com";
				};
			};
		};
	};
}