from conditions_controller_context import app

app.run(port=5002, debug=True, ssl_context=('certificates/cert.pem', 'certificates/key.pem'))
# app.run(host="0.0.0.0", port=8080, debug=True)
