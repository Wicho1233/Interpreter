from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .antlr_files.EvalVisitor import EvalVisitor
from antlr4 import *
from .antlr_files.MiniLangLexer import MiniLangLexer
from .antlr_files.MiniLangParser import MiniLangParser

def index(request):
    return render(request, 'minilang_app/index.html')

@csrf_exempt
def evaluate_code(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            code = data.get('code', '')
            
            # Evaluate the code
            visitor = EvalVisitor()
            input_stream = InputStream(code)
            lexer = MiniLangLexer(input_stream)
            token_stream = CommonTokenStream(lexer)
            parser = MiniLangParser(token_stream)
            tree = parser.program()
            result = visitor.visitProgram(tree)
            
            # Get the output from visitor
            output_lines = visitor.get_output()
            
            return JsonResponse({
                'success': True,
                'output': output_lines
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})