from django.shortcuts import render_to_response


def hello(request, *args):

    name = None
    if args:
        name = args[0].strip()[:-1]

    if not name:
        name = 'World'

    return render_to_response(
        'hello.html',
        {
            'name': name,
        },
    )
