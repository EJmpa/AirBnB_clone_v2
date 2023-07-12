# nginx_config.erb

$nginx_config = "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By ${hostname};
    root   /var/www/html;
    index index.html index.htm index.nginx-debian.html;
    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }
    location /redirect_me {
        return 301 http://linktr.ee/firdaus_h_salim/;
    }
    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}"


# web_server_setup.pp

package { 'nginx':
  ensure => installed,
}

file { '/data':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => true,
}

file { '/data/web_static':
  ensure => directory,
}

file { '/data/web_static/releases':
  ensure => directory,
}

file { '/data/web_static/shared':
  ensure => directory,
}

file { '/data/web_static/releases/test':
  ensure => directory,
}

file { '/data/web_static/releases/test/index.html':
  content => '<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>',
}

file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test',
}

file { '/etc/nginx/sites-available/default':
  ensure => present,
  content => $nginx_config,
  notify => Service['nginx'],
}

service { 'nginx':
  ensure => running,
  enable => true,
  require => File['/etc/nginx/sites-available/default'],
}

