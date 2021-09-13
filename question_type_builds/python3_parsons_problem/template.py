import json
SEPARATOR = "#<ab@17943918#@>#"
student_code = json.loads("""{{ STUDENT_ANSWER | e('py') }}""")["CR-parsons-code"][0]
exec(student_code)

{% for TEST in TESTCASES %}
{{ TEST.testcode }}
{% if not loop.last %}
print(SEPARATOR)
{% endif %}
{% endfor %}