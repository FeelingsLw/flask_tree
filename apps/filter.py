from apps import app

@app.template_filter
def gender(value):
    if value == "0" or value == 0:
        return '男'
    else:
        return '女'
