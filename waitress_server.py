from waitress import *
import main

serve(main, host='0.0.0.0', port=8080)