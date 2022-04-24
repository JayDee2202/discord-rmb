# Discord Role Merge Bot (DE)

Der Role Merge Bot führt Mitglieder einer von zwei Rollen in eine Rolle zusammen. Das ist zum Beispiel sinnvoll, wenn du Leute nur nach einer Rolle in der Mitgliederliste sortieren möchtest.
Diesen Fall könntest du bekommen, wenn auf deinem Server zwei Mitglieder mit Twitch-Integration aktiv sind und du alle Abonnenten auflisten möchtest.

Hierzu überwacht der Bot die beiden Quellrollen auf Veränderung. Sollte jemand neu in eine der beiden Rollen gelangen, wird der User auch der Zielrolle hinzugefügt. Sollte keine Mitgliedschaft mehr in einer der beiden Rollen bestehen, wird der User aus der Zielrolle entfernt.

Sicherheitshalber werden die Rollenmitgliedschaften einmal stündlich abgeglichen, falls der Bot offline war und Änderungen nicht live mitbekommen hat. 

## Verwendung

Zwingend angegeben benötigt der Bot mehrere Umgebungsvariablen:
- `DISCORD_ROLE_SOURCE1` - Rollen-ID der ersten Quell-Rolle
- `DISCORD_ROLE_SOURCE2` - Rollen-ID der zweiten Quell-Rolle
- `DISCORD_ROLE_DEST` - Rollen-ID der Ziel-Rolle
- `DISCORD_SERVER_ID` - Server-ID des Servers, benötigt für die Intents
- `DISCORD_TOKEN` - Token des Bots

Die IDs können per Rechtsklick auf die Rolle bzw. den Server und _ID kopieren_ herausgefunden werden. Sollte der Menüpunkt nicht bestehen, unter den erweiterten Einstellungen den _Entwicklermodus_ aktivieren.

Für den Bot-Token muss ein Bot im [Discord Developer Portal](https://discord.com/developers/applications) angelegt werden. Unter _Bot_ kann ein neuer Bot angelegt werden, zwingend erforderlich ist die Aktivierung der _Server Members Intent_.

### Image nutzen

Der Bot ist als fertig gebauter Container auf Docker Hub verfügbar unter dem Image-Namen `jaydee2202/discord-rmb:latest`. Für die Verwendung mit Docker Compose siehe das `docker-compose-image.yml`.

### Selbst bauen

Die `Dockerfile` als auch die `bot.py` liegen hier im Repository, ebenso kann auch mittels Docker Compose und der `docker-compose-build.yml` gebaut werden.


# Discord Role Merge Bot (EN)

The Role Merge Bot merges members of one of two roles into one role. This is useful, for example, if you want to sort people by only one role in the member list.
You might get this case if there are two members with Twitch integration active on your server and you want to list all subscribers in the member list.

To do this, the bot monitors the two source roles for change. If someone new joins one of the two roles, the user will also be added to the target role. If there is no more membership in either role, the user will be removed from the target role.

To be on the safe side, the role memberships are synchronized once an hour in case the bot was offline and did not notice any changes live. 


## Usage

Mandatory specified the bot needs several environment variables:
- `DISCORD_ROLE_SOURCE1` - role ID of the first source role
- `DISCORD_ROLE_SOURCE2` - role ID of the second source role
- `DISCORD_ROLE_DEST` - Role ID of the target role
- `DISCORD_SERVER_ID` - server ID of the server, needed for the intents
- `DISCORD_TOKEN` - token of the bot

The IDs can be found out by right-clicking on the role or server and _copy ID_. If the menu item does not exist, activate the _developer mode_ under the advanced settings.

For the bot token, a bot must be created in the [Discord Developer Portal](https://discord.com/developers/applications). Under _Bot_ a new bot can be created, it is mandatory to activate the _Server Members Intent_.

### Use image

The bot is available as a built container on Docker Hub under the image name `jaydee2202/discord-rmb:latest`. For use with Docker Compose, see the `docker-compose-image.yml`.

### Build it yourself

The `Dockerfile` as well as the `bot.py` are here in the repository, likewise you can also build using Docker Compose and the `docker-compose-build.yml`.


# Credits

Vielen Dank an @Breuxi für die Unterstützung!