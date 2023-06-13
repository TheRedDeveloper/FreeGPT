from main import app as application
config = {'host': '0.0.0.0', 'port': 1337, 'debug': True}
print(f"Running on port {config['port']}")
application.run(**config)
print(f"Closing port {config['port']}")
