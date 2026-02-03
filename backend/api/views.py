from django.shortcuts import render
import pandas as pd
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .serializers import UploadCSVSerializer
from .models import UploadHistory
from .serializers import UploadHistorySerializer
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import UploadHistory


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def report_pdf(request):
    last = UploadHistory.objects.order_by("-uploaded_at").first()

    if not last:
        # still return a valid PDF (not JSON), just with a message inside
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        w, h = A4

        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, h - 60, "CSV Report")
        c.setFont("Helvetica", 12)
        c.drawString(50, h - 90, "No uploads yet.")
        c.showPage()
        c.save()

        pdf = buffer.getvalue()
        buffer.close()

        resp = HttpResponse(pdf, content_type="application/pdf")
        resp["Content-Disposition"] = 'inline; filename="report.pdf"'
        return resp

    s = last.summary or {}

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    w, h = A4

    y = h - 60

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "CSV Report")
    y -= 25

    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Latest file: {last.filename}")
    y -= 18
    c.drawString(50, y, f"Uploaded at: {last.uploaded_at}")
    y -= 28

    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Latest Summary")
    y -= 18

    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Total equipment: {s.get('total_equipment', '-')}")
    y -= 16
    c.drawString(50, y, f"Avg flowrate: {s.get('avg_flowrate', '-')}")
    y -= 16
    c.drawString(50, y, f"Avg pressure: {s.get('avg_pressure', '-')}")
    y -= 16
    c.drawString(50, y, f"Avg temperature: {s.get('avg_temperature', '-')}")
    y -= 26

    dist = s.get("type_distribution", {}) or {}
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Type Distribution")
    y -= 18

    c.setFont("Helvetica", 12)
    if not dist:
        c.drawString(50, y, "No type_distribution found.")
        y -= 16
    else:
        for k, v in dist.items():
            if y < 80:  # new page safety
                c.showPage()
                y = h - 60
            c.drawString(60, y, f"{k}: {v}")
            y -= 16

    c.showPage()
    c.save()

    pdf = buffer.getvalue()
    buffer.close()

    resp = HttpResponse(pdf, content_type="application/pdf")
    resp["Content-Disposition"] = 'inline; filename="report.pdf"'
    return resp

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_csv(request):
    s = UploadCSVSerializer(data=request.data)
    s.is_valid(raise_exception=True)

    f = s.validated_data["file"]
    df = pd.read_csv(f)

    summary = {
        "total_equipment": len(df),
        "avg_flowrate": df["Flowrate"].mean(),
        "avg_pressure": df["Pressure"].mean(),
        "avg_temperature": df["Temperature"].mean(),
        "type_distribution": df["Type"].value_counts().to_dict(),
    }
    
    UploadHistory.objects.create(
        filename=f.name,
        summary=summary
    )
    
    keep_ids = UploadHistory.objects.order_by("-uploaded_at").values_list("id", flat=True)[:5]
    UploadHistory.objects.exclude(id__in=keep_ids).delete()

    
    return Response({"message": "uploaded"}, status=201)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def history_api(request):
    latest = UploadHistory.objects.order_by("-uploaded_at")[:5]
    s = UploadHistorySerializer(latest, many=True)
    return Response(s.data)
