"""
Application entry point.
"""
from hbnb.app import create_app
from hbnb.config import DevelopmentConfig
 
app = create_app('development')
 
if __name__ == '__main__':
    app.run(debug=True)
