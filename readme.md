# FastAPI project template

## Builds 

- Clone repository
- Fill the .env file following .env.example
- **Build the project** by typing
```
docker-compose up --build
```

- Or, if error occurs
```
sudo docker-compose up --build
```

### Migrations
To make manual migration, log into container using the commands below, then:
```
aerich migrate --name <migration_name>
```
To upgrade to latest version
```
aerich upgrade
```
To downgrade to specific version
```
aerich downgrade -h

Usage: aerich downgrade [OPTIONS]

  Downgrade to specified version.

Options:
  -v, --version INTEGER  Specified version, default to last.  [default: -1]
  -d, --delete           Delete version files at the same time.  [default:
                         False]

  --yes                  Confirm the action without prompting.
  -h, --help             Show this message and exit.
  ```

### Useful commands
log into container
```
docker exec -it <container_id> /bin/sh
```

To see running containers
```aidl
docker ps
```

To list docker volumes
```aidl
docker volume ls
```

To remove docker volume
```aidl
docker volume rm <number>
```

If error occurs in the above command run command below first
```aidl
docker container prune
```
