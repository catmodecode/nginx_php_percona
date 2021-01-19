FROM php:7.4.9-fpm-alpine3.12

WORKDIR /var/www

RUN apk upgrade --update && apk add --update --no-cache \
    autoconf \
    g++ \
    git \
    make \
    wget \
    curl \
    freetype \
    libpng \
    libjpeg-turbo \
    freetype-dev \
    libpng-dev \
    postgresql-dev \
    libjpeg-turbo-dev &&\
    docker-php-ext-configure gd \
        --with-freetype \
        --with-jpeg && \
    NPROC=$(grep -c ^processor /proc/cpuinfo 2>/dev/null || 1) && \
    docker-php-ext-install -j${NPROC} gd && \
    apk del --no-cache freetype-dev libpng-dev libjpeg-turbo-dev \
    libmcrypt-dev && \
    docker-php-ext-install -j$(nproc) pgsql && \
    docker-php-ext-install -j$(nproc) pdo_pgsql

RUN pecl install igbinary 
RUN docker-php-ext-enable igbinary

RUN pecl channel-update pecl.php.net && \
    # compile Redis with igbinary support
    pecl bundle redis && cd redis && phpize && ./configure --enable-redis-igbinary && make && make install && \
    docker-php-ext-enable igbinary redis && \
    docker-php-source delete && \
    rm -r /tmp/* /var/cache/*

RUN pecl install apcu
RUN docker-php-ext-enable apcu
RUN docker-php-ext-install bcmath

RUN apk add --update --no-cache libbz2 bzip2-dev

RUN docker-php-ext-install bz2
RUN docker-php-ext-install calendar
RUN docker-php-ext-install exif

RUN apk add --no-cache zip zlib-dev libzip-dev
RUN docker-php-ext-install zip

RUN apk add --no-cache gettext-dev
RUN docker-php-ext-install gettext

RUN apk add --no-cache icu-dev
RUN docker-php-ext-install intl

RUN apk add --no-cache libmemcached-dev
RUN pecl install memcached
RUN docker-php-ext-enable memcached

RUN pecl install msgpack
RUN docker-php-ext-enable msgpack
RUN docker-php-ext-install mysqli
RUN docker-php-ext-install pcntl
RUN docker-php-ext-install pdo_mysql

RUN pecl install protobuf
RUN docker-php-ext-enable protobuf
RUN docker-php-ext-install shmop

RUN apk add --no-cache libxml2-dev
RUN docker-php-ext-install soap
RUN docker-php-ext-install sockets
RUN docker-php-ext-install sysvmsg
RUN docker-php-ext-install sysvsem
RUN docker-php-ext-install sysvshm

RUN docker-php-ext-install opcache

RUN pecl install xdebug-2.9.6
RUN docker-php-ext-enable xdebug

RUN curl -sS https://getcomposer.org/installer | php -- \
        --filename=composer \
        --install-dir=/usr/local/bin && \
        echo "alias composer='composer'" >> /root/.bashrc

RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories;
ADD localhost.crt /etc/php/localhost.crt

RUN chown -R www-data:www-data ./

CMD ["php-fpm", "--nodaemonize"]
