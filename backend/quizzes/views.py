from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .quiz_generator import generate_quiz
from .models import Quiz, QuizAttempt
from courses.models import Lesson

class GenerateQuizView(APIView):
    def post(self, request):
        try:
            lesson_id = request.data.get('lesson_id')
            print(f"[DEBUG] Received lesson_id: {lesson_id}")
            
            if not lesson_id:
                return Response(
                    {'error': 'lesson_id is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            lesson = Lesson.objects.get(id=lesson_id)
            print(f"[DEBUG] Found lesson: {lesson.title}")
            
            # Generate quiz using Gemini AI
            print(f"[DEBUG] Generating quiz...")
            quiz_data = generate_quiz(
                topic=lesson.title,
                lesson_content=lesson.content,
                num_questions=request.data.get('num_questions', 5),
                difficulty=request.data.get('difficulty', 'medium')
            )
            print(f"[DEBUG] Quiz generated successfully")
            
            # Save quiz to database
            quiz = Quiz.objects.create(
                lesson=lesson,
                questions=quiz_data.dict()
            )
            print(f"[DEBUG] Quiz saved with ID: {quiz.id}")
            
            return Response({
                'quiz_id': quiz.id,
                'questions': [q.dict() for q in quiz_data.questions]
            }, status=status.HTTP_201_CREATED)
            
        except Lesson.DoesNotExist:
            print(f"[ERROR] Lesson with id {lesson_id} not found")
            return Response(
                {'error': f'Lesson with id {lesson_id} not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            print(f"[ERROR] Exception: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class SubmitQuizView(APIView):
    def post(self, request):
        quiz_id = request.data.get('quiz_id')
        user_answers = request.data.get('answers')  # Dict: {question_index: selected_option}
        
        quiz = Quiz.objects.get(id=quiz_id)
        questions = quiz.questions['questions']
        
        score = 0
        total = len(questions)
        results = []
        
        for idx, question in enumerate(questions):
            user_answer = user_answers.get(str(idx))
            correct = user_answer == question['correct_answer']
            if correct:
                score += 1
            
            results.append({
                'question_index': idx,
                'correct': correct,
                'user_answer': user_answer,
                'correct_answer': question['correct_answer'],
                'explanation': question['explanation']
            })
        
        # Save attempt
        QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
            total_questions=total,
            answers=user_answers,
            results=results
        )
        
        return Response({
            'score': score,
            'total': total,
            'percentage': (score/total) * 100,
            'results': results
        }, status=status.HTTP_200_OK)
