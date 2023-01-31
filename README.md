# BambuBot

BambuBot is a bot that tracks stocks for the Bambulab eu Filament store since everything is always out of stock.

# How to use

Use the docker compose file to run the bot. You can also run it without docker, but you will need to install the dependencies.

Set the bot `TOKEN` environment variable in the .env file like this:

```bash
TOKEN=a1b2c3d4e5f6g7h8i9j0a1b2c3d4e5f6g7h8i9j0a1b2c3d4e5f6g7h8i9j0
```

By default the bot will store data in the `data` folder. You can change this by setting the `DATA_PATH` environment variable.

Run the bot with docker-compose:

```bash
docker-compose up -d
```

# Commands

Send the commands as private messages to the bot.

```
!filaments - Check availability of all filaments
!notify - Enable notifications for a filament
```
