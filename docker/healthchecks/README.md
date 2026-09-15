# Health checks for Docker containers

## Postgres

On compose.yml:
```yaml
postgres:
  # ...
  healthcheck:
    start_period: 10s
    test:
      - "CMD-SHELL"
      - "pg_isready -U postgres || exit 1"
      # maybe use specific credentials and database
```

Or:
```yaml
#...
    test:
      - "CMD-SHELL"
      - "pg_isready -U $${POSTGRES_USER} -d $${POSTGRES_DB} || exit 1"
```

## Caddy

For Caddy let's check if Caddy is responding and ignore the reverse proxy target.

On Caddyfile:
```Caddy
{$DOMAIN_NAME} {
	route {
		reverse_proxy my_app_reverse_proxy:8000
	}
}

:7777 {
	respond "OK" 200
}
```

Then on compose.yml:
```yaml
caddy:
  image: caddy:2-alpine
  # ...
  healthcheck:
    start_period: 5s
    test:
      - "CMD-SHELL"
      - "curl -fsS http://127.0.0.1:7777/ >/dev/null"
```

### Possible issues

Caddy + wget for healthcheck on a non-https endpoint could result in spawing multiple *ssl_client* zombie processes. So avoid `wget --no-verbose --tries=1 --spider https://0.0.0.0:7777/`, unless you verify it.

Possible explanation: wget tries to do TLS to a non-TLS endpoint, which can trigger repeated failed SSL handshakes and subprocess cleanup issues. Links:

- https://github.com/caddyserver/caddy-docker/issues/276
- https://github.com/orgs/portainer/discussions/10314

## Redis

On compose.yml:
```yaml
redis:
  image: redis:7.4-alpine
  healthcheck:
    start_period: 5s
    test:
      - "CMD-SHELL"
      - "test $$(redis-cli ping) || exit 1"
```

## Celery

On compose.yml:
```yaml
celery:
  # 5.6.3
  # ...
  healthcheck:
    start_period: 10s
    test:
      - "CMD-SHELL"
      - "celery -A config.celery_app inspect ping || exit 1"
```

## Elasticsearch

On compose.yml:
```yaml
elasticsearch:
  image: docker.elastic.co/elasticsearch/elasticsearch-wolfi:9.3.3
  # ...
  healthcheck:
    start_period: 20s
    test:
      - "CMD-SHELL"
      - "curl -f http://localhost:9200/ || exit 1"
      # maybe http://localhost:9200/_cluster/health is better
```

## Generic check for permissions on a mounted volume

On compose.yml:
```yaml
app:
  # ...
  healthcheck:
    start_period: 10s
    test:
      - "CMD-SHELL"
      - "touch /data/healthcheck_testfile && rm /data/healthcheck_testfile || exit 1"
```
