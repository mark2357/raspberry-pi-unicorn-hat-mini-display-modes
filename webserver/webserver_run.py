import web






print(__name__)
render = web.template.render('templates/')

urls = (
    '/', 'index',

)

class index:
    def GET(self):
        # return "Hello, world!"
        return render.index()

    def POST(self):
        data = web.data() # you can get data use this method
        # print(data)
        test()
        raise web.seeother('/')

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
    print('test')

# webserver_run()



def test():
    print('testing 123')