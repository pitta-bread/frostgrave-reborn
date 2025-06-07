from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI()


# function definition using Django-Ninja default router
@api.get("/hello")
def hello(request):
    return "Hello world"
