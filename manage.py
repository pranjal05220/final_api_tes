from aiprofile_api import create_app
from flask_script import Manager
from flask_script.commands import ShowUrls, Clean

from aiprofile_api import HookServer

app = create_app()
manager = Manager(app)

manager.add_command("server", HookServer())
manager.add_command("show-urls", ShowUrls())
manager.add_command("clean", Clean())


if __name__ == "__main__":
    manager.run()

