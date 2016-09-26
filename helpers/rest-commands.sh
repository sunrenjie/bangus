# login, token and cookies (token and session-id combined)
credential=(email=user@g.cn password=user)
x=$(http 127.0.0.1:8000/api/v1/auth/login/ ${credential[0]} ${credential[1]} -h | sed 's/;//g' | \
  awk 'BEGIN{s=""}$1=="Set-Cookie:"{ s = s$2";"; if($2~/^csrftoken=/) { print "__"$2 }}END{print "Cookie:"s}' | \
  sed 's/__csrftoken=/X-CSRFToken:/' |xargs echo)
y=($x)

# list projects
http --print=HhBb 127.0.0.1:8000/api/v1/projects/ ${y[0]} ${y[1]}

# create a new one from json loaded from file(content: {"name": "user-project-5"}); no owner info needed since that is
# available in the login session.
http --print=HhBb 127.0.0.1:8000/api/v1/projects/ ${y[0]} ${y[1]} @t1.json


# delete the project; shall not work
http --print=HhBb DELETE 127.0.0.1:8000/api/v1/projects/94db4cc44d5e4cbb99bdd35a4e085c19/ ${y[0]} ${y[1]}
