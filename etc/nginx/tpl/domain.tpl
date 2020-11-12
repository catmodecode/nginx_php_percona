server {
    server_name #domain#;
    include /etc/nginx/ssl_redirect.conf;
}

server {
    server_name #domain#;
    listen 443 ssl;

    include /etc/nginx/cert.conf;

    access_log  /var/log/nginx/#domain#.access.log;
    error_log  /var/log/nginx/#domain#.error.log;

    set $root_path /var/www/#domain#;

    server_tokens off;

    #error_page 404  = /404.php;
    error_page 500  = /500.php;

    index index.php index.htm index.html;

    include       /etc/nginx/locations.conf;

}