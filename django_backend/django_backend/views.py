from django.shortcuts import render 
import requests
import subprocess
from django.http import JsonResponse

def compileFile(request):
    # data = requests.get("https://reqres.in/api/users")
    # print(data.text)
    # return render(request, )

    try:
        result = subprocess.run(
            ["python", "custom_prog_lang2/parser.py"],
            capture_output=True, text = True
        )
        return JsonResponse({
            "success": True, 
            "output": result.stdout, 
            "error": result.stderr
        })
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})