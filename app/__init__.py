from flask import Flask


app=Flask(__name__)
# 导入config
app.config.from_object("config")
from app import views