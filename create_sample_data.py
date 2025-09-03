#!/usr/bin/env python
# Sample data creation script for Telegram Market Bot

import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telegram_market.settings')
django.setup()

from templates.models import Category, Template
from users.models import User

# Create categories
categories_data = [
    {
        'name': 'E-commerce',
        'slug': 'ecommerce',
        'description': 'Complete shopping bot templates with cart functionality, payment integration, and order tracking.',
        'icon': 'fas fa-shopping-cart'
    },
    {
        'name': 'Customer Support',
        'slug': 'customer-support',
        'description': 'Professional customer service bots with ticket systems, FAQ handling, and live chat integration.',
        'icon': 'fas fa-headset'
    },
    {
        'name': 'Entertainment',
        'slug': 'entertainment',
        'description': 'Fun and engaging bots for games, quizzes, music, and interactive entertainment.',
        'icon': 'fas fa-gamepad'
    },
    {
        'name': 'Business Tools',
        'slug': 'business-tools',
        'description': 'Productivity bots for project management, scheduling, analytics, and business automation.',
        'icon': 'fas fa-briefcase'
    },
    {
        'name': 'Education',
        'slug': 'education',
        'description': 'Learning platform bots with courses, quizzes, progress tracking, and educational content.',
        'icon': 'fas fa-graduation-cap'
    },
    {
        'name': 'Utilities',
        'slug': 'utilities',
        'description': 'Helpful utility bots for weather, currency conversion, file processing, and daily tools.',
        'icon': 'fas fa-tools'
    }
]

print("Creating categories...")
for cat_data in categories_data:
    category, created = Category.objects.get_or_create(
        slug=cat_data['slug'],
        defaults=cat_data
    )
    if created:
        print(f"✓ Created category: {category.name}")
    else:
        print(f"- Category already exists: {category.name}")

# Create sample templates
templates_data = [
    {
        'title': 'Advanced E-commerce Bot',
        'slug': 'advanced-ecommerce-bot',
        'short_description': 'Complete shopping experience with cart, payments, and order tracking.',
        'description': 'A comprehensive e-commerce bot template that includes product catalog, shopping cart functionality, multiple payment gateways, order tracking, customer support integration, and admin dashboard. Perfect for online stores and marketplaces.',
        'price': 49.99,
        'category_slug': 'ecommerce',
        'features': ['Product Catalog', 'Shopping Cart', 'Payment Integration', 'Order Tracking', 'Admin Dashboard', 'Customer Support'],
        'demo_available': True,
        'active': True
    },
    {
        'title': 'AI Customer Support Bot',
        'slug': 'ai-customer-support-bot',
        'short_description': 'Intelligent customer service with AI-powered responses and ticket system.',
        'description': 'Advanced customer support bot with AI-powered response generation, ticket management system, escalation to human agents, knowledge base integration, and comprehensive analytics. Reduce support workload by 80%.',
        'price': 39.99,
        'category_slug': 'customer-support',
        'features': ['AI Responses', 'Ticket System', 'Human Escalation', 'Knowledge Base', 'Analytics', 'Multi-language'],
        'demo_available': True,
        'active': True
    },
    {
        'title': 'Interactive Quiz Bot',
        'slug': 'interactive-quiz-bot',
        'short_description': 'Engaging quiz platform with leaderboards and custom questions.',
        'description': 'Fun and interactive quiz bot with customizable questions, multiple choice and text answers, real-time leaderboards, user statistics, achievements system, and social sharing features.',
        'price': 19.99,
        'category_slug': 'entertainment',
        'features': ['Custom Questions', 'Leaderboards', 'Achievements', 'Statistics', 'Social Sharing', 'Multiple Game Modes'],
        'demo_available': True,
        'active': True
    },
    {
        'title': 'Project Management Bot',
        'slug': 'project-management-bot',
        'short_description': 'Complete project tracking with tasks, deadlines, and team collaboration.',
        'description': 'Professional project management bot with task creation and assignment, deadline tracking, team collaboration tools, progress reports, file sharing, and integration with popular project management platforms.',
        'price': 59.99,
        'category_slug': 'business-tools',
        'features': ['Task Management', 'Team Collaboration', 'Deadline Tracking', 'Progress Reports', 'File Sharing', 'Platform Integration'],
        'demo_available': False,
        'active': True
    },
    {
        'title': 'Learning Management System',
        'slug': 'learning-management-system',
        'short_description': 'Educational platform with courses, quizzes, and progress tracking.',
        'description': 'Comprehensive learning management system bot with course creation, video lessons, interactive quizzes, progress tracking, certificates, and student-teacher communication features.',
        'price': 79.99,
        'category_slug': 'education',
        'features': ['Course Creation', 'Video Lessons', 'Interactive Quizzes', 'Progress Tracking', 'Certificates', 'Communication Tools'],
        'demo_available': True,
        'active': True
    },
    {
        'title': 'Weather & Currency Bot',
        'slug': 'weather-currency-bot',
        'short_description': 'Real-time weather updates and currency conversion with notifications.',
        'description': 'Utility bot providing real-time weather information, currency conversion, exchange rate alerts, weather notifications, location-based services, and historical data tracking.',
        'price': 14.99,
        'category_slug': 'utilities',
        'features': ['Real-time Weather', 'Currency Conversion', 'Rate Alerts', 'Location Services', 'Historical Data', 'Notifications'],
        'demo_available': True,
        'active': True
    },
    {
        'title': 'Subscription Management Bot',
        'slug': 'subscription-management-bot',
        'short_description': 'Automated subscription handling with payments and renewals.',
        'description': 'Advanced subscription management bot with automated billing, payment processing, subscription renewals, customer notifications, analytics dashboard, and integration with major payment providers.',
        'price': 69.99,
        'category_slug': 'business-tools',
        'features': ['Automated Billing', 'Payment Processing', 'Renewal Management', 'Customer Notifications', 'Analytics', 'Payment Integration'],
        'demo_available': False,
        'active': True
    },
    {
        'title': 'Social Media Manager',
        'slug': 'social-media-manager',
        'short_description': 'Schedule posts, track engagement, and manage multiple platforms.',
        'description': 'Comprehensive social media management bot for scheduling posts, tracking engagement metrics, managing multiple platforms, content curation, hashtag suggestions, and performance analytics.',
        'price': 44.99,
        'category_slug': 'business-tools',
        'features': ['Post Scheduling', 'Engagement Tracking', 'Multi-platform', 'Content Curation', 'Hashtag Suggestions', 'Analytics'],
        'demo_available': True,
        'active': True
    }
]

print("\nCreating templates...")
for template_data in templates_data:
    category = Category.objects.get(slug=template_data['category_slug'])
    
    template, created = Template.objects.get_or_create(
        slug=template_data['slug'],
        defaults={
            'title': template_data['title'],
            'short_description': template_data['short_description'],
            'description': template_data['description'],
            'price': template_data['price'],
            'category': category,
            'features': template_data['features'],
            'demo_available': template_data['demo_available'],
            'active': template_data['active']
        }
    )
    
    if created:
        print(f"✓ Created template: {template.title}")
    else:
        print(f"- Template already exists: {template.title}")

print(f"\nSample data creation completed!")
print(f"Categories created: {Category.objects.count()}")
print(f"Templates created: {Template.objects.count()}")
print(f"Admin user: admin / admin123")