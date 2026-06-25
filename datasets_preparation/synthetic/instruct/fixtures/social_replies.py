SOCIAL_REPLY_FIXTURES = {
    'affirmative_scheduling': {
        'prompt_templates': [
            'Write one short friendly reply to this message:\n{message}',
            'Write one short friendly reply to this message:\n{message}\nOnly provide the reply.',
            'Reply in a friendly way to this message:\n{message}\nOnly provide the reply.',
            'Write a short text reply:\n{message}\nOnly provide the reply.',
            'Draft a friendly text message reply as the recipient:\n{message}\nOnly provide the reply.',
            'Write a friendly reply as the recipient:\n{message}\nOnly provide the reply.',
        ],
        'examples': [
            {
                'message': 'Can we meet tomorrow?',
                'answer': 'Sure, tomorrow works for me.',
            },
            {
                'message': 'Are you free this weekend?',
                'answer': 'Yes, I should be free this weekend.',
            },
            {
                'message': 'Can we move the call to Friday?',
                'answer': 'Sure, Friday works for me.',
            },
            {
                'message': 'Do you want to grab coffee this afternoon?',
                'answer': 'Sure, coffee this afternoon sounds good.',
            },
            {
                'message': 'Can we talk after lunch?',
                'answer': 'Sure, after lunch works for me.',
            },
            {
                'message': 'Would Tuesday morning work for you?',
                'answer': 'Yes, Tuesday morning works for me.',
            },
            {'message': 'Can we meet at 3?', 'answer': 'Yes, 3 works for me.'},
            {
                'message': 'Should we catch up next week?',
                'answer': 'Yes, that sounds good.',
            },
            {
                'message': 'Do you want to join the study session tonight?',
                'answer': 'Sure, I would be happy to join.',
            },
            {
                'message': 'Can I call you later today?',
                'answer': 'Yes, feel free to call me later.',
            },
            {
                'message': 'Can we have lunch tomorrow?',
                'answer': 'Sure, lunch tomorrow sounds good.',
            },
            {
                'message': 'Would you like to go for a walk after work?',
                'answer': 'Yes, that would be nice.',
            },
            {
                'message': 'Can we meet before the workshop?',
                'answer': 'Sure, meeting before the workshop works for me.',
            },
            {
                'message': 'Do you want to work on the project together tomorrow?',
                'answer': 'Yes, working on it together tomorrow sounds good.',
            },
            {
                'message': 'Can we meet after class?',
                'answer': 'Sure, after class works for me.',
            },
            {
                'message': 'Would you like to study together later?',
                'answer': 'Yes, studying together later sounds good.',
            },
            {
                'message': 'Can we schedule a quick chat tomorrow?',
                'answer': 'Sure, a quick chat tomorrow works for me.',
            },
            {
                'message': 'Do you want to meet at the cafe?',
                'answer': 'Sure, meeting at the cafe sounds good.',
            },
            {
                'message': 'Can we catch up this afternoon?',
                'answer': 'Yes, this afternoon works for me.',
            },
            {
                'message': 'Would lunch on Friday work?',
                'answer': 'Yes, lunch on Friday works for me.',
            },
        ],
    },
    'thanks': {
        'prompt_templates': [
            'Write one short friendly reply to this message:\n{message}',
            'Write one short friendly reply to this message:\n{message}\nOnly provide the reply.',
            'Reply in a friendly way to this message:\n{message}\nOnly provide the reply.',
            'Write a short text reply:\n{message}\nOnly provide the reply.',
            'Draft a friendly text message reply as the recipient:\n{message}\nOnly provide the reply.',
            'Write a warm reply as the recipient:\n{message}\nOnly provide the reply.',
        ],
        'examples': [
            {
                'message': 'Thanks for your help!',
                'answer': "You're welcome, happy to help!",
            },
            {
                'message': 'Thank you for sending the notes.',
                'answer': "You're welcome, glad they were useful.",
            },
            {
                'message': 'I really appreciate your time today.',
                'answer': "You're very welcome, I was glad to help.",
            },
            {
                'message': 'Thanks for checking this so quickly.',
                'answer': 'No problem, happy to help.',
            },
            {
                'message': 'Thanks for explaining that to me.',
                'answer': "You're welcome, I am glad it helped.",
            },
            {
                'message': 'Thanks for being patient with me.',
                'answer': 'Of course, no worries at all.',
            },
            {
                'message': 'Thank you for the birthday message.',
                'answer': 'Thank you, that was very kind of you.',
            },
            {
                'message': 'Good luck with your presentation.',
                'answer': 'Thank you, I really appreciate it.',
            },
            {
                'message': 'Thanks for making time for me.',
                'answer': "You're welcome, I was happy to make time.",
            },
            {
                'message': 'Thank you for reviewing my draft.',
                'answer': "You're welcome, I was happy to review it.",
            },
            {
                'message': 'Thanks for listening.',
                'answer': "Of course, I'm glad you told me.",
            },
            {
                'message': 'Thank you for helping me today.',
                'answer': "You're welcome, I was happy to help.",
            },
            {
                'message': 'Thanks for the quick reply.',
                'answer': 'No problem, happy to help.',
            },
            {
                'message': 'I appreciate your advice.',
                'answer': "You're welcome, I hope it helps.",
            },
            {
                'message': 'Thanks for reminding me.',
                'answer': "You're welcome, glad I could help.",
            },
        ],
    },
    'apology_ack': {
        'prompt_templates': [
            'Write one short friendly reply to this message:\n{message}',
            'Write one short friendly reply to this message:\n{message}\nOnly provide the reply.',
            'Reply in a friendly way to this message:\n{message}\nOnly provide the reply.',
            'Write a kind reply to this message:\n{message}\nOnly provide the reply.',
            'Draft a friendly text message reply as the recipient:\n{message}\nOnly provide the reply.',
            'Write a friendly reply as the recipient:\n{message}\nOnly provide the reply.',
        ],
        'examples': [
            {
                'message': 'Sorry, I forgot to reply earlier.',
                'answer': 'No problem, thanks for getting back to me.',
            },
            {
                'message': 'Sorry, I am running late.',
                'answer': 'No worries, thanks for letting me know.',
            },
            {
                'message': 'Sorry for the confusion.',
                'answer': 'No worries, thanks for clearing it up.',
            },
            {
                'message': 'Sorry, I missed your call.',
                'answer': 'No problem, we can talk later.',
            },
            {
                'message': 'Sorry I could not make it today.',
                'answer': 'No worries, I hope everything is okay.',
            },
            {
                'message': 'Sorry, I sent the wrong file.',
                'answer': 'No problem, thanks for sending the right one.',
            },
            {
                'message': 'Sorry for the late notice.',
                'answer': 'No worries, thanks for telling me.',
            },
            {
                'message': 'Sorry, today has been really busy.',
                'answer': 'No worries, I completely understand.',
            },
            {
                'message': 'Sorry I forgot to send the notes.',
                'answer': 'No problem, you can send them when you have time.',
            },
            {
                'message': 'Sorry, I made a mistake in the document.',
                'answer': 'No worries, mistakes happen.',
            },
            {
                'message': 'Sorry I did not see this earlier.',
                'answer': 'No problem, thanks for replying now.',
            },
            {
                'message': 'Sorry, I misunderstood the plan.',
                'answer': 'No worries, we can sort it out.',
            },
            {
                'message': 'Sorry I was late to the meeting.',
                'answer': 'No worries, thanks for joining.',
            },
            {
                'message': 'Sorry, I forgot our call.',
                'answer': 'No problem, we can reschedule.',
            },
            {
                'message': 'Sorry I could not help earlier.',
                'answer': 'No worries, I appreciate you getting back to me.',
            },
        ],
    },
    'celebration': {
        'prompt_templates': [
            'Write one short friendly reply to this message:\n{message}',
            'Write one short friendly reply to this message:\n{message}\nOnly provide the reply.',
            'Reply in a cheerful way to this message:\n{message}\nOnly provide the reply.',
            'Write a warm reply to this message:\n{message}\nOnly provide the reply.',
            'Draft a friendly text message reply as the recipient:\n{message}\nOnly provide the reply.',
            'Write a friendly reply as the recipient:\n{message}\nOnly provide the reply.',
        ],
        'examples': [
            {
                'message': 'I passed the exam!',
                'answer': "That's wonderful news, congratulations!",
            },
            {
                'message': 'I got the job!',
                'answer': "That's amazing, congratulations!",
            },
            {
                'message': 'I finished the project!',
                'answer': 'Great work, that is exciting news!',
            },
            {
                'message': 'I won the competition!',
                'answer': "That's fantastic, congratulations!",
            },
            {
                'message': 'My presentation went really well!',
                'answer': "That's great to hear, well done!",
            },
            {
                'message': 'I finally solved the bug!',
                'answer': 'Nice work, that must feel great.',
            },
            {
                'message': 'I got accepted into the course!',
                'answer': "That's brilliant news, congratulations!",
            },
            {
                'message': 'I reached my goal today!',
                'answer': "That's wonderful, I am really happy for you.",
            },
            {
                'message': 'I received great feedback from the team!',
                'answer': "That's excellent, you deserve it.",
            },
            {
                'message': 'I completed my first marathon!',
                'answer': "That's incredible, congratulations!",
            },
            {
                'message': 'I got my first research result working!',
                'answer': "That's exciting, great work!",
            },
            {
                'message': 'The demo worked perfectly!',
                'answer': 'Amazing, I am glad it went so well.',
            },
            {
                'message': 'I finally finished my essay!',
                'answer': 'Great job, that must feel so good.',
            },
            {
                'message': 'I got a great score on the test!',
                'answer': "That's fantastic, congratulations!",
            },
            {
                'message': 'My interview went really well!',
                'answer': "That's great news, well done!",
            },
            {
                'message': 'I fixed the last bug!',
                'answer': 'Nice work, that is a big win.',
            },
            {
                'message': 'I submitted the project!',
                'answer': 'Great work, congratulations on finishing it.',
            },
            {
                'message': 'I learned how to build the model!',
                'answer': "That's exciting, great progress!",
            },
        ],
    },
    'supportive_nervous': {
        'prompt_templates': [
            'Write one short friendly reply to this message:\n{message}',
            'Write one short supportive reply to this message:\n{message}',
            'Reply in a supportive way to this message:\n{message}\nOnly provide the reply.',
            'Write a kind reply to this message:\n{message}\nOnly provide the reply.',
            'Draft a supportive friendly reply as the recipient:\n{message}\nOnly provide the reply.',
            'Write a supportive reply as the recipient:\n{message}\nOnly provide the reply.',
        ],
        'examples': [
            {
                'message': 'I am feeling nervous about the meeting.',
                'answer': "You've got this, and I hope it goes well.",
            },
            {
                'message': 'I am worried about the exam tomorrow.',
                'answer': "I know it feels stressful, but you've prepared well.",
            },
            {
                'message': 'I am not sure I can do this.',
                'answer': 'You can do this, just take it one step at a time.',
            },
            {
                'message': 'I feel overwhelmed today.',
                'answer': 'I am sorry today feels heavy. Take it one step at a time.',
            },
            {
                'message': 'I am scared about the interview.',
                'answer': "That's understandable, but I believe you can handle it.",
            },
            {
                'message': 'I do not think my presentation is good enough.',
                'answer': 'I know it is hard to judge your own work, but I think you are doing well.',
            },
            {
                'message': 'I am having a rough day.',
                'answer': 'I am sorry it has been rough. I hope things get easier soon.',
            },
            {
                'message': 'I am nervous about sharing my work.',
                'answer': 'That is completely understandable, but your work is worth sharing.',
            },
            {
                'message': 'I feel like I messed everything up.',
                'answer': 'I am sorry you feel that way, but one mistake does not define everything.',
            },
            {
                'message': 'I am worried people will not like my idea.',
                'answer': 'That is a normal worry, but your idea is worth discussing.',
            },
            {
                'message': 'I feel stuck on this task.',
                'answer': 'That happens sometimes. Take a short break and try one small step.',
            },
            {
                'message': 'I am anxious about tomorrow.',
                'answer': 'I am sorry you are feeling anxious. I hope tomorrow goes smoothly.',
            },
            {
                'message': 'I am worried about my presentation.',
                'answer': "That's understandable, but I think you will do well.",
            },
            {
                'message': 'I do not know if I can finish this.',
                'answer': 'Take it one step at a time. You can make progress.',
            },
            {
                'message': 'I feel nervous about asking a question.',
                'answer': 'That is understandable, but asking questions is a good way to learn.',
            },
            {
                'message': 'I am stressed about the deadline.',
                'answer': 'That sounds stressful. Focus on the next small step.',
            },
            {
                'message': 'I am afraid I will make a mistake.',
                'answer': 'Mistakes happen, and you can still do well.',
            },
        ],
    },
    'cancellation_ack': {
        'prompt_templates': [
            'Write one short friendly reply to this message:\n{message}',
            'Write one short friendly reply to this message:\n{message}\nOnly provide the reply.',
            'Reply in a friendly way to this message:\n{message}\nOnly provide the reply.',
            'Write a kind reply to this message:\n{message}\nOnly provide the reply.',
            'Draft a friendly text message reply as the recipient:\n{message}\nOnly provide the reply.',
            'Write a friendly reply as the recipient:\n{message}\nOnly provide the reply.',
        ],
        'examples': [
            {
                'message': 'I need to cancel today.',
                'answer': 'No problem, we can find another time.',
            },
            {
                'message': 'Can we reschedule our meeting?',
                'answer': 'Of course, we can reschedule.',
            },
            {
                'message': 'Something came up, so I cannot make it.',
                'answer': 'No worries, thanks for letting me know.',
            },
            {
                'message': 'I have to move our call to next week.',
                'answer': 'No problem, next week works for me.',
            },
            {
                'message': 'I cannot attend the session today.',
                'answer': 'No worries, thanks for telling me.',
            },
            {
                'message': 'Can we postpone lunch?',
                'answer': 'Sure, we can do lunch another time.',
            },
            {
                'message': 'I need to leave early today.',
                'answer': 'No problem, thanks for letting me know.',
            },
            {
                'message': 'I cannot join the call anymore.',
                'answer': 'No worries, we can catch up later.',
            },
            {
                'message': 'Can we move dinner to another day?',
                'answer': 'Sure, another day works for me.',
            },
            {
                'message': 'I need to cancel because I am not feeling well.',
                'answer': 'No problem, I hope you feel better soon.',
            },
            {
                'message': 'Can we move our meeting to next week?',
                'answer': 'Sure, next week works for me.',
            },
            {
                'message': 'I have to cancel our coffee today.',
                'answer': 'No problem, we can go another time.',
            },
            {
                'message': 'I cannot make it to the call.',
                'answer': 'No worries, thanks for letting me know.',
            },
            {
                'message': 'Can we delay the meeting by an hour?',
                'answer': 'Sure, delaying by an hour works for me.',
            },
            {
                'message': 'I need to reschedule our study session.',
                'answer': 'No problem, we can reschedule it.',
            },
        ],
    },
    'request_ack': {
        'prompt_templates': [
            'Write one short friendly reply to this message:\n{message}',
            'Write one short friendly reply to this message:\n{message}\nOnly provide the reply.',
            'Reply in a friendly way to this message:\n{message}\nOnly provide the reply.',
            'Write a short text reply:\n{message}\nOnly provide the reply.',
            'Draft a friendly text message reply as the recipient:\n{message}\nOnly provide the reply.',
            'Write a friendly reply as the recipient:\n{message}\nOnly provide the reply.',
        ],
        'examples': [
            {
                'message': 'Can you send me the notes later?',
                'answer': 'Sure, I can send them later.',
            },
            {
                'message': 'Can you check this when you have time?',
                'answer': 'Of course, I will take a look when I can.',
            },
            {
                'message': 'Can you review my draft?',
                'answer': 'Sure, I can review it.',
            },
            {
                'message': 'Can you remind me tomorrow?',
                'answer': 'Sure, I can remind you tomorrow.',
            },
            {
                'message': 'Can you share the link with me?',
                'answer': 'Sure, I will send you the link.',
            },
            {
                'message': 'Can you help me with this later?',
                'answer': 'Of course, I can help later.',
            },
            {
                'message': 'Can you look over the slides?',
                'answer': 'Sure, I can look over the slides.',
            },
            {
                'message': 'Can you send the agenda before the meeting?',
                'answer': 'Sure, I will send the agenda before the meeting.',
            },
            {
                'message': 'Can you let me know when you arrive?',
                'answer': 'Sure, I will let you know when I arrive.',
            },
            {
                'message': 'Can you take a look at this bug?',
                'answer': 'Sure, I can take a look at the bug.',
            },
            {
                'message': 'Can you explain this part again?',
                'answer': 'Of course, I can explain it again.',
            },
            {
                'message': 'Can you send me the address?',
                'answer': 'Sure, I will send you the address.',
            },
            {
                'message': 'Can you check my answer?',
                'answer': 'Sure, I can check it.',
            },
            {
                'message': 'Can you send me the file?',
                'answer': 'Sure, I will send you the file.',
            },
            {
                'message': 'Can you remind me about the meeting?',
                'answer': 'Sure, I can remind you about the meeting.',
            },
            {
                'message': 'Can you look at this later today?',
                'answer': 'Of course, I can look at it later today.',
            },
            {
                'message': 'Can you help me prepare?',
                'answer': 'Sure, I can help you prepare.',
            },
            {
                'message': 'Can you read this when you have a minute?',
                'answer': 'Sure, I can read it when I have a minute.',
            },
        ],
    },
}
SOCIAL_REPLY_FIXTURES = {
    'affirmative_scheduling': {
        'prompt_templates': [
            'Write one short friendly reply to this message:\n{message}',
            'Write one short friendly reply to this message:\n{message}\nOnly provide the reply.',
            'Reply in a friendly way to this message:\n{message}\nOnly provide the reply.',
            'Write a short text reply:\n{message}\nOnly provide the reply.',
            'Draft a friendly text message reply as the recipient:\n{message}\nOnly provide the reply.',
            'Write a friendly reply as the recipient:\n{message}\nOnly provide the reply.',
        ],
        'examples': [
            {
                'message': 'Can we meet tomorrow?',
                'answer': 'Sure, tomorrow works for me.',
            },
            {
                'message': 'Are you free this weekend?',
                'answer': 'Yes, I should be free this weekend.',
            },
            {
                'message': 'Can we move the call to Friday?',
                'answer': 'Sure, Friday works for me.',
            },
            {
                'message': 'Do you want to grab coffee this afternoon?',
                'answer': 'Sure, coffee this afternoon sounds good.',
            },
            {
                'message': 'Can we talk after lunch?',
                'answer': 'Sure, after lunch works for me.',
            },
            {
                'message': 'Would Tuesday morning work for you?',
                'answer': 'Yes, Tuesday morning works for me.',
            },
            {'message': 'Can we meet at 3?', 'answer': 'Yes, 3 works for me.'},
            {
                'message': 'Should we catch up next week?',
                'answer': 'Yes, that sounds good.',
            },
            {
                'message': 'Do you want to join the study session tonight?',
                'answer': 'Sure, I would be happy to join.',
            },
            {
                'message': 'Can I call you later today?',
                'answer': 'Yes, feel free to call me later.',
            },
            {
                'message': 'Can we have lunch tomorrow?',
                'answer': 'Sure, lunch tomorrow sounds good.',
            },
            {
                'message': 'Would you like to go for a walk after work?',
                'answer': 'Yes, that would be nice.',
            },
            {
                'message': 'Can we meet before the workshop?',
                'answer': 'Sure, meeting before the workshop works for me.',
            },
            {
                'message': 'Do you want to work on the project together tomorrow?',
                'answer': 'Yes, working on it together tomorrow sounds good.',
            },
            {
                'message': 'Can we meet after class?',
                'answer': 'Sure, after class works for me.',
            },
            {
                'message': 'Would you like to study together later?',
                'answer': 'Yes, studying together later sounds good.',
            },
            {
                'message': 'Can we schedule a quick chat tomorrow?',
                'answer': 'Sure, a quick chat tomorrow works for me.',
            },
            {
                'message': 'Do you want to meet at the cafe?',
                'answer': 'Sure, meeting at the cafe sounds good.',
            },
            {
                'message': 'Can we catch up this afternoon?',
                'answer': 'Yes, this afternoon works for me.',
            },
            {
                'message': 'Would lunch on Friday work?',
                'answer': 'Yes, lunch on Friday works for me.',
            },
        ],
    },
    'thanks': {
        'prompt_templates': [
            'Write one short friendly reply to this message:\n{message}',
            'Write one short friendly reply to this message:\n{message}\nOnly provide the reply.',
            'Reply in a friendly way to this message:\n{message}\nOnly provide the reply.',
            'Write a short text reply:\n{message}\nOnly provide the reply.',
            'Draft a friendly text message reply as the recipient:\n{message}\nOnly provide the reply.',
            'Write a warm reply as the recipient:\n{message}\nOnly provide the reply.',
        ],
        'examples': [
            {
                'message': 'Thanks for your help!',
                'answer': "You're welcome, happy to help!",
            },
            {
                'message': 'Thank you for sending the notes.',
                'answer': "You're welcome, glad they were useful.",
            },
            {
                'message': 'I really appreciate your time today.',
                'answer': "You're very welcome, I was glad to help.",
            },
            {
                'message': 'Thanks for checking this so quickly.',
                'answer': 'No problem, happy to help.',
            },
            {
                'message': 'Thanks for explaining that to me.',
                'answer': "You're welcome, I am glad it helped.",
            },
            {
                'message': 'Thanks for being patient with me.',
                'answer': 'Of course, no worries at all.',
            },
            {
                'message': 'Thank you for the birthday message.',
                'answer': 'Thank you, that was very kind of you.',
            },
            {
                'message': 'Good luck with your presentation.',
                'answer': 'Thank you, I really appreciate it.',
            },
            {
                'message': 'Thanks for making time for me.',
                'answer': "You're welcome, I was happy to make time.",
            },
            {
                'message': 'Thank you for reviewing my draft.',
                'answer': "You're welcome, I was happy to review it.",
            },
            {
                'message': 'Thanks for listening.',
                'answer': "Of course, I'm glad you told me.",
            },
            {
                'message': 'Thank you for helping me today.',
                'answer': "You're welcome, I was happy to help.",
            },
            {
                'message': 'Thanks for the quick reply.',
                'answer': 'No problem, happy to help.',
            },
            {
                'message': 'I appreciate your advice.',
                'answer': "You're welcome, I hope it helps.",
            },
            {
                'message': 'Thanks for reminding me.',
                'answer': "You're welcome, glad I could help.",
            },
        ],
    },
    'apology_ack': {
        'prompt_templates': [
            'Write one short friendly reply to this message:\n{message}',
            'Write one short friendly reply to this message:\n{message}\nOnly provide the reply.',
            'Reply in a friendly way to this message:\n{message}\nOnly provide the reply.',
            'Write a kind reply to this message:\n{message}\nOnly provide the reply.',
            'Draft a friendly text message reply as the recipient:\n{message}\nOnly provide the reply.',
            'Write a friendly reply as the recipient:\n{message}\nOnly provide the reply.',
        ],
        'examples': [
            {
                'message': 'Sorry, I forgot to reply earlier.',
                'answer': 'No problem, thanks for getting back to me.',
            },
            {
                'message': 'Sorry, I am running late.',
                'answer': 'No worries, thanks for letting me know.',
            },
            {
                'message': 'Sorry for the confusion.',
                'answer': 'No worries, thanks for clearing it up.',
            },
            {
                'message': 'Sorry, I missed your call.',
                'answer': 'No problem, we can talk later.',
            },
            {
                'message': 'Sorry I could not make it today.',
                'answer': 'No worries, I hope everything is okay.',
            },
            {
                'message': 'Sorry, I sent the wrong file.',
                'answer': 'No problem, thanks for sending the right one.',
            },
            {
                'message': 'Sorry for the late notice.',
                'answer': 'No worries, thanks for telling me.',
            },
            {
                'message': 'Sorry, today has been really busy.',
                'answer': 'No worries, I completely understand.',
            },
            {
                'message': 'Sorry I forgot to send the notes.',
                'answer': 'No problem, you can send them when you have time.',
            },
            {
                'message': 'Sorry, I made a mistake in the document.',
                'answer': 'No worries, mistakes happen.',
            },
            {
                'message': 'Sorry I did not see this earlier.',
                'answer': 'No problem, thanks for replying now.',
            },
            {
                'message': 'Sorry, I misunderstood the plan.',
                'answer': 'No worries, we can sort it out.',
            },
            {
                'message': 'Sorry I was late to the meeting.',
                'answer': 'No worries, thanks for joining.',
            },
            {
                'message': 'Sorry, I forgot our call.',
                'answer': 'No problem, we can reschedule.',
            },
            {
                'message': 'Sorry I could not help earlier.',
                'answer': 'No worries, I appreciate you getting back to me.',
            },
        ],
    },
    'celebration': {
        'prompt_templates': [
            'Write one short friendly reply to this message:\n{message}',
            'Write one short friendly reply to this message:\n{message}\nOnly provide the reply.',
            'Reply in a cheerful way to this message:\n{message}\nOnly provide the reply.',
            'Write a warm reply to this message:\n{message}\nOnly provide the reply.',
            'Draft a friendly text message reply as the recipient:\n{message}\nOnly provide the reply.',
            'Write a friendly reply as the recipient:\n{message}\nOnly provide the reply.',
        ],
        'examples': [
            {
                'message': 'I passed the exam!',
                'answer': "That's wonderful news, congratulations!",
            },
            {
                'message': 'I got the job!',
                'answer': "That's amazing, congratulations!",
            },
            {
                'message': 'I finished the project!',
                'answer': 'Great work, that is exciting news!',
            },
            {
                'message': 'I won the competition!',
                'answer': "That's fantastic, congratulations!",
            },
            {
                'message': 'My presentation went really well!',
                'answer': "That's great to hear, well done!",
            },
            {
                'message': 'I finally solved the bug!',
                'answer': 'Nice work, that must feel great.',
            },
            {
                'message': 'I got accepted into the course!',
                'answer': "That's brilliant news, congratulations!",
            },
            {
                'message': 'I reached my goal today!',
                'answer': "That's wonderful, I am really happy for you.",
            },
            {
                'message': 'I received great feedback from the team!',
                'answer': "That's excellent, you deserve it.",
            },
            {
                'message': 'I completed my first marathon!',
                'answer': "That's incredible, congratulations!",
            },
            {
                'message': 'I got my first research result working!',
                'answer': "That's exciting, great work!",
            },
            {
                'message': 'The demo worked perfectly!',
                'answer': 'Amazing, I am glad it went so well.',
            },
            {
                'message': 'I finally finished my essay!',
                'answer': 'Great job, that must feel so good.',
            },
            {
                'message': 'I got a great score on the test!',
                'answer': "That's fantastic, congratulations!",
            },
            {
                'message': 'My interview went really well!',
                'answer': "That's great news, well done!",
            },
            {
                'message': 'I fixed the last bug!',
                'answer': 'Nice work, that is a big win.',
            },
            {
                'message': 'I submitted the project!',
                'answer': 'Great work, congratulations on finishing it.',
            },
            {
                'message': 'I learned how to build the model!',
                'answer': "That's exciting, great progress!",
            },
        ],
    },
    'supportive_nervous': {
        'prompt_templates': [
            'Write one short friendly reply to this message:\n{message}',
            'Write one short supportive reply to this message:\n{message}',
            'Reply in a supportive way to this message:\n{message}\nOnly provide the reply.',
            'Write a kind reply to this message:\n{message}\nOnly provide the reply.',
            'Draft a supportive friendly reply as the recipient:\n{message}\nOnly provide the reply.',
            'Write a supportive reply as the recipient:\n{message}\nOnly provide the reply.',
        ],
        'examples': [
            {
                'message': 'I am feeling nervous about the meeting.',
                'answer': "You've got this, and I hope it goes well.",
            },
            {
                'message': 'I am worried about the exam tomorrow.',
                'answer': "I know it feels stressful, but you've prepared well.",
            },
            {
                'message': 'I am not sure I can do this.',
                'answer': 'You can do this, just take it one step at a time.',
            },
            {
                'message': 'I feel overwhelmed today.',
                'answer': 'I am sorry today feels heavy. Take it one step at a time.',
            },
            {
                'message': 'I am scared about the interview.',
                'answer': "That's understandable, but I believe you can handle it.",
            },
            {
                'message': 'I do not think my presentation is good enough.',
                'answer': 'I know it is hard to judge your own work, but I think you are doing well.',
            },
            {
                'message': 'I am having a rough day.',
                'answer': 'I am sorry it has been rough. I hope things get easier soon.',
            },
            {
                'message': 'I am nervous about sharing my work.',
                'answer': 'That is completely understandable, but your work is worth sharing.',
            },
            {
                'message': 'I feel like I messed everything up.',
                'answer': 'I am sorry you feel that way, but one mistake does not define everything.',
            },
            {
                'message': 'I am worried people will not like my idea.',
                'answer': 'That is a normal worry, but your idea is worth discussing.',
            },
            {
                'message': 'I feel stuck on this task.',
                'answer': 'That happens sometimes. Take a short break and try one small step.',
            },
            {
                'message': 'I am anxious about tomorrow.',
                'answer': 'I am sorry you are feeling anxious. I hope tomorrow goes smoothly.',
            },
            {
                'message': 'I am worried about my presentation.',
                'answer': "That's understandable, but I think you will do well.",
            },
            {
                'message': 'I do not know if I can finish this.',
                'answer': 'Take it one step at a time. You can make progress.',
            },
            {
                'message': 'I feel nervous about asking a question.',
                'answer': 'That is understandable, but asking questions is a good way to learn.',
            },
            {
                'message': 'I am stressed about the deadline.',
                'answer': 'That sounds stressful. Focus on the next small step.',
            },
            {
                'message': 'I am afraid I will make a mistake.',
                'answer': 'Mistakes happen, and you can still do well.',
            },
        ],
    },
    'cancellation_ack': {
        'prompt_templates': [
            'Write one short friendly reply to this message:\n{message}',
            'Write one short friendly reply to this message:\n{message}\nOnly provide the reply.',
            'Reply in a friendly way to this message:\n{message}\nOnly provide the reply.',
            'Write a kind reply to this message:\n{message}\nOnly provide the reply.',
            'Draft a friendly text message reply as the recipient:\n{message}\nOnly provide the reply.',
            'Write a friendly reply as the recipient:\n{message}\nOnly provide the reply.',
        ],
        'examples': [
            {
                'message': 'I need to cancel today.',
                'answer': 'No problem, we can find another time.',
            },
            {
                'message': 'Can we reschedule our meeting?',
                'answer': 'Of course, we can reschedule.',
            },
            {
                'message': 'Something came up, so I cannot make it.',
                'answer': 'No worries, thanks for letting me know.',
            },
            {
                'message': 'I have to move our call to next week.',
                'answer': 'No problem, next week works for me.',
            },
            {
                'message': 'I cannot attend the session today.',
                'answer': 'No worries, thanks for telling me.',
            },
            {
                'message': 'Can we postpone lunch?',
                'answer': 'Sure, we can do lunch another time.',
            },
            {
                'message': 'I need to leave early today.',
                'answer': 'No problem, thanks for letting me know.',
            },
            {
                'message': 'I cannot join the call anymore.',
                'answer': 'No worries, we can catch up later.',
            },
            {
                'message': 'Can we move dinner to another day?',
                'answer': 'Sure, another day works for me.',
            },
            {
                'message': 'I need to cancel because I am not feeling well.',
                'answer': 'No problem, I hope you feel better soon.',
            },
            {
                'message': 'Can we move our meeting to next week?',
                'answer': 'Sure, next week works for me.',
            },
            {
                'message': 'I have to cancel our coffee today.',
                'answer': 'No problem, we can go another time.',
            },
            {
                'message': 'I cannot make it to the call.',
                'answer': 'No worries, thanks for letting me know.',
            },
            {
                'message': 'Can we delay the meeting by an hour?',
                'answer': 'Sure, delaying by an hour works for me.',
            },
            {
                'message': 'I need to reschedule our study session.',
                'answer': 'No problem, we can reschedule it.',
            },
        ],
    },
    'request_ack': {
        'prompt_templates': [
            'Write one short friendly reply to this message:\n{message}',
            'Write one short friendly reply to this message:\n{message}\nOnly provide the reply.',
            'Reply in a friendly way to this message:\n{message}\nOnly provide the reply.',
            'Write a short text reply:\n{message}\nOnly provide the reply.',
            'Draft a friendly text message reply as the recipient:\n{message}\nOnly provide the reply.',
            'Write a friendly reply as the recipient:\n{message}\nOnly provide the reply.',
        ],
        'examples': [
            {
                'message': 'Can you send me the notes later?',
                'answer': 'Sure, I can send them later.',
            },
            {
                'message': 'Can you check this when you have time?',
                'answer': 'Of course, I will take a look when I can.',
            },
            {
                'message': 'Can you review my draft?',
                'answer': 'Sure, I can review it.',
            },
            {
                'message': 'Can you remind me tomorrow?',
                'answer': 'Sure, I can remind you tomorrow.',
            },
            {
                'message': 'Can you share the link with me?',
                'answer': 'Sure, I will send you the link.',
            },
            {
                'message': 'Can you help me with this later?',
                'answer': 'Of course, I can help later.',
            },
            {
                'message': 'Can you look over the slides?',
                'answer': 'Sure, I can look over the slides.',
            },
            {
                'message': 'Can you send the agenda before the meeting?',
                'answer': 'Sure, I will send the agenda before the meeting.',
            },
            {
                'message': 'Can you let me know when you arrive?',
                'answer': 'Sure, I will let you know when I arrive.',
            },
            {
                'message': 'Can you take a look at this bug?',
                'answer': 'Sure, I can take a look at the bug.',
            },
            {
                'message': 'Can you explain this part again?',
                'answer': 'Of course, I can explain it again.',
            },
            {
                'message': 'Can you send me the address?',
                'answer': 'Sure, I will send you the address.',
            },
            {
                'message': 'Can you check my answer?',
                'answer': 'Sure, I can check it.',
            },
            {
                'message': 'Can you send me the file?',
                'answer': 'Sure, I will send you the file.',
            },
            {
                'message': 'Can you remind me about the meeting?',
                'answer': 'Sure, I can remind you about the meeting.',
            },
            {
                'message': 'Can you look at this later today?',
                'answer': 'Of course, I can look at it later today.',
            },
            {
                'message': 'Can you help me prepare?',
                'answer': 'Sure, I can help you prepare.',
            },
            {
                'message': 'Can you read this when you have a minute?',
                'answer': 'Sure, I can read it when I have a minute.',
            },
        ],
    },
}
