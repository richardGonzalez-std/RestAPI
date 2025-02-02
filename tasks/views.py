from django.shortcuts import render, get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from .filters import TaskFilter
from .models import *
from drf_spectacular.utils import extend_schema
import csv
from reportlab.pdfgen import canvas
from openpyxl import Workbook
from .serializers import *

    

    
# Create your views here.


class TaskListRetrieveUpdateDeleteAPIView(GenericAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    def get(self,request,pk):
        task = get_object_or_404(Task,pk=pk,user=request.user)
        serializer = self.serializer_class(task)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

    def put(self,request,pk):
        task = get_object_or_404(Task,pk=pk,user=request.user)
        serializer = self.serializer_class(task,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request,pk):
        task = get_object_or_404(Task, pk = pk, user = request.user)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class TaskGetAllAndPost(GenericAPIView):
    serializer_class = TaskSerializer
    def get(self,request):
        tasks = Task.objects.all()
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ExportApiAsCSV(GenericAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_superuser:
            return self.export_csv(request)
        
        return Response(
            {"detail": f'{request.user} no tiene los permisos necesarios'},
            status=status.HTTP_400_BAD_REQUEST
        )

    def export_csv(self,request):
        tasks = Task.objects.all()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="tasks.csv"'
        writer = csv.writer(response)
        writer.writerows([['ID',"Title"],["Description","Deadline","Completed"]])

        for task in tasks:
            writer.writerows([[
                task.id,
                task.title,
                task.description,
                task.deadline,
                task.completed]
            ])
        return response
    
    



class TaskExportExcel(GenericAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if request.user.is_superuser:
            return self.export_excel(request)
    
    def export_excel(self,request):
        tasks = Task.objects.all()
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Exported Tareas"
        sheet.append(['ID','Título','Descripción','Completado'])

        for task in tasks:
            sheet.append([
                task.id,
                task.title,
                task.description,
                task.completed
            ])

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = "attachment; filename=tasks.xlsx"
        workbook.save(response)
        return response

class TaskExportPDF(GenericAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if request.user.is_superuser:
            return self.export_pdf(request)
    def export_pdf(self,request):
        tasks = Task.objects.all()
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=tasks.pdf'
        
        p = canvas.Canvas(response)
        p.setFont('Helvetica',12)
        p.drawString(100,800,"Lista de Tareas")

        y = 750

        for task in tasks:
            p.drawString(100, y, f"Tarea:{task.title} - Completada: {task.completed} - ")
            y -= 20

        p.save()
        return response
class TaskListFilteredAPIView(GenericAPIView):
    serializer_class=TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter

    def get(self,request):
        tasks = TaskFilter(request.GET, queryset=Task.objects.filter(user=request.user))
        serializer = self.serializer_class(tasks)
        return Response(serializer.data, status)
    
    
    
