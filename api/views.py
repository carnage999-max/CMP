from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import QuestionSerializer
from main.models import QuizQuestion


@api_view(['GET'])
def getQuestions(request):
    questions = QuizQuestion.objects.all()
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getQuestionsByCourseCode(request, course_code):
    questions = QuizQuestion.objects.filter(course_code=course_code)
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getAllCourses(request):  
    courses_avail = set()
    questtions = QuizQuestion.objects.all()
    for q in questtions:
        courses_avail.add(q.course_code)
    return Response({"courses": list(courses_avail)})

@api_view(["POST"])
def answerQuestion(request, answer):
    user_answer = QuestionSerializer(answer)


@api_view(['POST'])
def markQuestion(request, answer):
    pass
