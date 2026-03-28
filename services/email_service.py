"""
Email Service
- Send task reminder emails using SMTP
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Tuple
import os
from abc import ABC, abstractmethod


class EmailService:
    """Service for sending emails via SMTP"""
    
    def __init__(self):
        """Initialize email service with credentials from environment variables"""
        self.sender_email = os.getenv('EMAIL_USER', '')
        self.sender_password = os.getenv('EMAIL_PASS', '')
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
    
    def send_email(self, to_email: str, subject: str, message: str, is_html: bool = True) -> Tuple[bool, str]:
        """
        Send an email to the specified recipient
        
        Args:
            to_email: Recipient email address
            subject: Email subject line
            message: Email body content
            is_html: Whether the message is HTML formatted (default: True)
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        
        # Validate credentials
        if not self.sender_email or not self.sender_password:
            return False, "Email credentials not configured. Set EMAIL_USER and EMAIL_PASS environment variables."
        
        # Validate email address
        if not self._validate_email(to_email):
            return False, f"Invalid recipient email address: {to_email}"
        
        try:
            # Create email message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.sender_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Attach message
            mime_type = 'html' if is_html else 'plain'
            part = MIMEText(message, mime_type)
            msg.attach(part)
            
            # Create SMTP session
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Enable secure connection
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            return True, f"Email sent successfully to {to_email}"
        
        except smtplib.SMTPAuthenticationError:
            return False, "SMTP Authentication failed. Check EMAIL_USER and EMAIL_PASS."
        except smtplib.SMTPException as e:
            return False, f"SMTP error occurred: {str(e)}"
        except Exception as e:
            return False, f"Error sending email: {str(e)}"
    
    def send_task_reminder(self, to_email: str, task_name: str, reminder_message: str) -> Tuple[bool, str]:
        """
        Send a task reminder email
        
        Args:
            to_email: Recipient email address
            task_name: Name of the task
            reminder_message: The reminder message content
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        subject = f"Task Reminder: {task_name}"
        
        # Format as HTML email for better presentation
        html_message = self._format_html_email(task_name, reminder_message)
        
        return self.send_email(to_email, subject, html_message, is_html=True)
    
    def _format_html_email(self, task_name: str, message: str) -> str:
        """Format email as HTML for better presentation"""
        # Convert line breaks to HTML
        formatted_message = message.replace('\n', '<br>')
        
        html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="background-color: #f5f5f5; padding: 20px; border-radius: 5px;">
                    <h2 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;">
                        📋 {task_name}
                    </h2>
                    <div style="background-color: white; padding: 20px; border-radius: 3px; margin-top: 15px;">
                        {formatted_message}
                    </div>
                    <div style="margin-top: 20px; padding-top: 10px; border-top: 1px solid #ddd; font-size: 12px; color: #666;">
                        <p>This is an automated message from AI Meeting Intelligence System.</p>
                    </div>
                </div>
            </body>
        </html>
        """
        return html
    
    def _validate_email(self, email: str) -> bool:
        """Validate email address format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None


# Initialize service instance
email_service = EmailService()


def send_email(to_email: str, subject: str, message: str) -> Tuple[bool, str]:
    """
    Convenience function to send an email
    
    Args:
        to_email: Recipient email address
        subject: Email subject line
        message: Email body content
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    return email_service.send_email(to_email, subject, message)


def send_task_reminder(to_email: str, task_name: str, reminder_message: str) -> Tuple[bool, str]:
    """
    Convenience function to send a task reminder email
    
    Args:
        to_email: Recipient email address
        task_name: Name of the task
        reminder_message: The reminder message content
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    return email_service.send_task_reminder(to_email, task_name, reminder_message)
