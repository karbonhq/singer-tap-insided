
ENDPOINTS_CONFIG = {
    'articles': {
        'path': '/v2/articles',
        'pk': ['id'],
        'provides': {
            'article_id': 'id'
        },
        'children': {
            'article_replies': {
                'path': '/v2/articles/{article_id}/replies',
                'pk': ['id']
            },
            'article_poll_results': {
                'paginate': False,
                'path': '/v2/articles/{article_id}/poll',
                'pk': ['article_id'],
                'http_statuses_to_ignore': [404]
            }
        }
    },
    ## These are 500'ing
    # 'articles_trashed': {
    #     'path': '/v2/articles/trashed',
    #     'pk': ['id'],
    #     'schema_filename': 'articles.json'
    # },
    # 'article_drafts': {
    #     'path': '/v2/articles/drafts',
    #     'pk': ['id'],
    #     'schema_filename': 'articles.json'
    # },
    'conversations': {
        'path': '/v2/conversations',
        'pk': ['id'],
        'provides': {
            'conversation_id': 'id'
        },
        'children': {
            'conversation_replies': {
                'path': '/v2/conversations/{conversation_id}/replies',
                'pk': ['id']
            }
        }
    },
    ## This is 500'ing
    # 'conversations_trashed': {
    #     'path': '/v2/conversations/trashed',
    #     'pk': ['id'],
    #     'schema_filename': 'conversations.json'
    # },
    'events': {
        'path': '/v2/events',
        'pk': ['id']
    },
    'questions': {
        'path': '/v2/questions',
        'pk': ['id'],
        'provides': {
            'question_id': 'id'
        },
        'children': {
            'question_replies': {
                'path': '/v2/questions/{question_id}/replies',
                'pk': ['id']
            }
        }
    },
    ## This is 500'ing
    # 'questions_trashed': {
    #     'path': '/v2/questions/trashed',
    #     'pk': ['id'],
    #     'schema_filename': 'questions.json'
    # },
    'topics': {
        'path': '/v2/topics',
        'pk': ['id']
    },
    'tags': {
        'path': '/v2/tags',
        'pk': ['id']
    },
    'categories': {
        'path': '/v2/categories',
        'pk': ['id'],
        'provides': {
            'category_id': 'id'
        },
        # 'children': {
        #     'category_topics': {
        #         'path': '/v2/categories/{category_id}/topics',
        #         'pk': ['id'],
        #         'schema_filename': 'topics.json'
        #     }
        # }
    },
    # 'product_areas': {
    #     'path': '/v2/productAreas',
    #     'pk': ['id']
    # },
    'product_updates': {
        'path': '/v2/productUpdates',
        'pk': ['id'],
        'provides': {
            'product_update_id': 'id'
        },
        'children': {
            'product_update_replies': {
                'path': '/v2/productUpdates/{product_update_id}/replies',
                'pk': ['id']
            }
        }
    },
    # 'product_updates_trashed': {
    #     'path': '/v2/productUpdates/trashed',
    #     'pk': ['id'],
    #     'schema_filename': 'product_updates.json'
    # },
    # 'product_update_drafts': {
    #     'path': '/v2/productUpdates/drafts',
    #     'pk': ['id'],
    #     'schema_filename': 'product_updates.json'
    # },
    'users': {
        'path': '/user',
        'pk': ['userid'],
        'number_indexed': True
    },
    'user_activities': {
        'path': '/user/activity',
        'pk': ['event_uuid'],
        'number_indexed': True
    }
}
