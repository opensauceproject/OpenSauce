# config valid for current version and patch releases of Capistrano
lock "~> 3.11.0"

set :application, "OpenSauce"
set :repo_url, "git@github.com:HE-Arc/OpenSauce.git"

after 'deploy:updating', 'python:create_venv'
after 'deploy:updated', 'django:collect_static'
after 'deploy:updated', 'django:migrate'
# after 'deploy:updated', 'django:setProd'
after 'deploy:publishing', 'uwsgi:restart'

namespace :uwsgi do
    desc "Restart application"
    task :restart do
        on roles(:web) do |h|
          execute :sudo, "rm -f ~/www/logs/uwsgi.log"
	        execute :sudo, "sv reload uwsgi nginx daphne"
	   end
    end
end

namespace :python do

    def venv_path
        File.join(shared_path, "venv")
    end

    desc "Create venv"
    task :create_venv do
        on roles([:app, :web]) do |h|
	    execute "rm -rf #{venv_path}"
	    execute "python -m venv #{venv_path}"
	    execute "source #{venv_path}/bin/activate"
        execute "#{venv_path}/bin/pip install -r #{release_path}/requirements.txt"
        end
    end
end

namespace :django do
# thanks PayPixPlace
# thanks Synai
    desc 'Migrate'
    task :migrate do
        on roles([:app, :web]) do |h|
        execute "#{venv_path}/bin/python #{release_path}/manage.py migrate"
        end
    end

    desc 'Collect static files'
    task :collect_static do
        on roles([:app, :web]) do |h|
        execute "#{venv_path}/bin/python #{release_path}/manage.py collectstatic --noinput"
        end
    end

    desc 'Set debug to False'
    task :setProd do
        on roles([:app, :web]) do |h|
        execute "sed -i 's/DEBUG = True/DEBUG = False/g' #{release_path}/Synai/settings.py"
        end
    end
end
# Default branch is :master
# ask :branch, `git rev-parse --abbrev-ref HEAD`.chomp

# Default deploy_to directory is /var/www/my_app_name
# set :deploy_to, "/var/www/my_app_name"

# Default value for :format is :airbrussh.
# set :format, :airbrussh

# You can configure the Airbrussh format using :format_options.
# These are the defaults.
# set :format_options, command_output: true, log_file: "log/capistrano.log", color: :auto, truncate: :auto

# Default value for :pty is false
# set :pty, true

# Default value for :linked_files is []
# append :linked_files, "config/database.yml"

# Default value for linked_dirs is []
# append :linked_dirs, "log", "tmp/pids", "tmp/cache", "tmp/sockets", "public/system"

# Default value for default_env is {}
# set :default_env, { path: "/opt/ruby/bin:$PATH" }

# Default value for local_user is ENV['USER']
# set :local_user, -> { `git config user.name`.chomp }

# Default value for keep_releases is 5
# set :keep_releases, 5

# Uncomment the following to require manually verifying the host key before first deploy.
# set :ssh_options, verify_host_key: :secure
