from cushy_storage import CushyOrmCache, BaseORMModel

orm_cache = CushyOrmCache()


class User(BaseORMModel):

    def __init__(self, name, age):
        super().__init__()
        self.name = name
        self.age = age


def init_data():
    for i in range(10):
        orm_cache.add(User("jack", 18))


if __name__ == '__main__':
    init_data()
    orm_cache.remove_duplicates(User)
    users = orm_cache.query(User).all()
    for i, user in enumerate(users):
        print(i, user.name)