from conditions_controller_context import app
app.run(port=5003, debug=True, ssl_context=('certificates/cert.pem', 'certificates/key.pem'))