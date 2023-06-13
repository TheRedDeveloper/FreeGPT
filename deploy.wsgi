project_home = '/home/RedDeveloper/mysite'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path
from main import app as application
