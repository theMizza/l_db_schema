from django.shortcuts import render
from django.db import connection
from .forms import MakeSQLQueryForm


def sql_executor(request):
    results = []
    columns = []
    error = None
    form = MakeSQLQueryForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        try:
            query = form.cleaned_data['query']
            with connection.cursor() as cursor:
                cursor.execute(query)
                if cursor.description:
                    columns = [col[0] for col in cursor.description]
                    results = cursor.fetchall()
        except Exception as e:
            error = f"Ошибка выполнения запроса: {e}"

    return render(request, 'app.html', {
        'form': form,
        'results': results,
        'columns': columns,
        'error': error
    })