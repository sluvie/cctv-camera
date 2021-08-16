from app import app ## import app dari package app yang kita buat
import uuid

app.secret_key = "sub-camera" # str(uuid.uuid4())
app.run(host="0.0.0.0", port="4002",debug=False)