SOCIAL_REPLY_FIXTURES = {
    'affirmative_scheduling': {
        'examples': [
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nCan we meet tomorrow?\nOnly provide the reply.',
                'answer': 'Sure, tomorrow works for me.',
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nAre you free this weekend?\nOnly provide the reply.',
                'answer': 'Yes, I should be free this weekend.',
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nCan we move the call to Friday?\nOnly provide the reply.',
                'answer': 'Sure, Friday works for me.',
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nDo you want to grab coffee this afternoon?\nOnly provide the reply.',
                'answer': 'Sure, coffee this afternoon sounds good.',
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nCan we talk after lunch?\nOnly provide the reply.',
                'answer': 'Sure, after lunch works for me.',
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nWould Tuesday morning work for you?\nOnly provide the reply.',
                'answer': 'Yes, Tuesday morning works for me.',
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nCan we meet at 3?\nOnly provide the reply.',
                'answer': 'Yes, 3 works for me.',
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nShould we catch up next week?\nOnly provide the reply.',
                'answer': 'Yes, that sounds good.',
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nDo you want to join the study session tonight?\nOnly provide the reply.',
                'answer': 'Sure, I would be happy to join.',
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nCan I call you later today?\nOnly provide the reply.',
                'answer': 'Yes, feel free to call me later.',
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nCan we have lunch tomorrow?\nOnly provide the reply.',
                'answer': 'Sure, lunch tomorrow sounds good.',
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nWould you like to go for a walk after work?\nOnly provide the reply.',
                'answer': 'Yes, that would be nice.',
            },
            {
                'prompt': 'Draft a warm reply as the recipient:\nCan we meet before the workshop?\nOnly provide the reply.',
                'answer': 'Sure, meeting before the workshop works for me.',
            },
            {
                'prompt': 'Write a friendly reply as the recipient:\nDo you want to work on the project together tomorrow?\nOnly provide the reply.',
                'answer': 'Yes, working on it together tomorrow sounds good.',
            },
        ],
    },

    'thanks': {
        'examples': [
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nThanks for your help!\nOnly provide the reply.',
                'answer': "You're welcome, happy to help!",
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nThank you for sending the notes.\nOnly provide the reply.',
                'answer': "You're welcome, glad they were useful.",
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nI really appreciate your time today.\nOnly provide the reply.',
                'answer': "You're very welcome, I was glad to help.",
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nThanks for checking this so quickly.\nOnly provide the reply.',
                'answer': 'No problem, happy to help.',
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nThanks for explaining that to me.\nOnly provide the reply.',
                'answer': "You're welcome, I am glad it helped.",
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nThanks for being patient with me.\nOnly provide the reply.',
                'answer': 'Of course, no worries at all.',
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nThank you for the birthday message.\nOnly provide the reply.',
                'answer': 'Thank you, that was very kind of you.',
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nGood luck with your presentation.\nOnly provide the reply.',
                'answer': 'Thank you, I really appreciate it.',
            },
            {
                'prompt': 'Draft a warm reply as the recipient:\nThanks for making time for me.\nOnly provide the reply.',
                'answer': "You're welcome, I was happy to make time.",
            },
            {
                'prompt': 'Write a friendly reply as the recipient:\nThank you for reviewing my draft.\nOnly provide the reply.',
                'answer': "You're welcome, I was happy to review it.",
            },
        ],
    },

    'apology_ack': {
        'examples': [
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nSorry, I forgot to reply earlier.\nOnly provide the reply.',
                'answer': 'No problem, thanks for getting back to me.',
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nSorry, I am running late.\nOnly provide the reply.',
                'answer': 'No worries, thanks for letting me know.',
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nSorry for the confusion.\nOnly provide the reply.',
                'answer': 'No worries, thanks for clearing it up.',
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nSorry, I missed your call.\nOnly provide the reply.',
                'answer': 'No problem, we can talk later.',
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nSorry I could not make it today.\nOnly provide the reply.',
                'answer': 'No worries, I hope everything is okay.',
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nSorry, I sent the wrong file.\nOnly provide the reply.',
                'answer': 'No problem, thanks for sending the right one.',
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nSorry for the late notice.\nOnly provide the reply.',
                'answer': 'No worries, thanks for telling me.',
            },
            {
                'prompt': 'Draft a warm reply as the recipient:\nSorry, today has been really busy.\nOnly provide the reply.',
                'answer': 'No worries, I completely understand.',
            },
            {
                'prompt': 'Write a friendly reply as the recipient:\nSorry I forgot to send the notes.\nOnly provide the reply.',
                'answer': 'No problem, you can send them when you have time.',
            },
            {
                'prompt': 'Write a kind reply as the recipient:\nSorry, I made a mistake in the document.\nOnly provide the reply.',
                'answer': 'No worries, mistakes happen.',
            },
        ],
    },

    'celebration': {
        'examples': [
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nI passed the exam!\nOnly provide the reply.',
                'answer': "That's wonderful news, congratulations!",
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nI got the job!\nOnly provide the reply.',
                'answer': "That's amazing, congratulations!",
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nI finished the project!\nOnly provide the reply.',
                'answer': 'Great work, that is exciting news!',
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nI won the competition!\nOnly provide the reply.',
                'answer': "That's fantastic, congratulations!",
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nMy presentation went really well!\nOnly provide the reply.',
                'answer': "That's great to hear, well done!",
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nI finally solved the bug!\nOnly provide the reply.',
                'answer': 'Nice work, that must feel great.',
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nI got accepted into the course!\nOnly provide the reply.',
                'answer': "That's brilliant news, congratulations!",
            },
            {
                'prompt': 'Draft a warm reply as the recipient:\nI reached my goal today!\nOnly provide the reply.',
                'answer': "That's wonderful, I am really happy for you.",
            },
            {
                'prompt': 'Write a friendly reply as the recipient:\nI received great feedback from the team!\nOnly provide the reply.',
                'answer': "That's excellent, you deserve it.",
            },
            {
                'prompt': 'Write a cheerful reply as the recipient:\nI completed my first marathon!\nOnly provide the reply.',
                'answer': "That's incredible, congratulations!",
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nI got my first research result working!\nOnly provide the reply.',
                'answer': "That's exciting, great work!",
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nThe demo worked perfectly!\nOnly provide the reply.',
                'answer': 'Amazing, I am glad it went so well.',
            },
        ],
    },

    'supportive_nervous': {
        'examples': [
            {
                'prompt': 'Draft a supportive friendly reply as the recipient:\nI am feeling nervous about the meeting.\nOnly provide the reply.',
                'answer': "You've got this, and I hope it goes well.",
            },
            {
                'prompt': 'Draft a supportive friendly reply as the recipient:\nI am worried about the exam tomorrow.\nOnly provide the reply.',
                'answer': "I know it feels stressful, but you've prepared well.",
            },
            {
                'prompt': 'Draft a supportive friendly reply as the recipient:\nI am not sure I can do this.\nOnly provide the reply.',
                'answer': 'You can do this, just take it one step at a time.',
            },
            {
                'prompt': 'Draft a supportive friendly reply as the recipient:\nI feel overwhelmed today.\nOnly provide the reply.',
                'answer': 'I am sorry today feels heavy. Take it one step at a time.',
            },
            {
                'prompt': 'Draft a supportive friendly reply as the recipient:\nI am scared about the interview.\nOnly provide the reply.',
                'answer': "That's understandable, but I believe you can handle it.",
            },
            {
                'prompt': 'Draft a supportive friendly reply as the recipient:\nI do not think my presentation is good enough.\nOnly provide the reply.',
                'answer': 'I know it is hard to judge your own work, but I think you are doing well.',
            },
            {
                'prompt': 'Draft a supportive friendly reply as the recipient:\nI am having a rough day.\nOnly provide the reply.',
                'answer': 'I am sorry it has been rough. I hope things get easier soon.',
            },
            {
                'prompt': 'Draft a supportive friendly reply as the recipient:\nI am nervous about sharing my work.\nOnly provide the reply.',
                'answer': 'That is completely understandable, but your work is worth sharing.',
            },
            {
                'prompt': 'Write a kind reply as the recipient:\nI feel like I messed everything up.\nOnly provide the reply.',
                'answer': 'I am sorry you feel that way, but one mistake does not define everything.',
            },
            {
                'prompt': 'Write a supportive reply as the recipient:\nI am worried people will not like my idea.\nOnly provide the reply.',
                'answer': 'That is a normal worry, but your idea is worth discussing.',
            },
            {
                'prompt': 'Draft a warm reply as the recipient:\nI feel stuck on this task.\nOnly provide the reply.',
                'answer': 'That happens sometimes. Take a short break and try one small step.',
            },
            {
                'prompt': 'Draft a supportive friendly reply as the recipient:\nI am anxious about tomorrow.\nOnly provide the reply.',
                'answer': 'I am sorry you are feeling anxious. I hope tomorrow goes smoothly.',
            },
        ],
    },

    'cancellation_ack': {
        'examples': [
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nI need to cancel today.\nOnly provide the reply.',
                'answer': 'No problem, we can find another time.',
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nCan we reschedule our meeting?\nOnly provide the reply.',
                'answer': 'Of course, we can reschedule.',
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nSomething came up, so I cannot make it.\nOnly provide the reply.',
                'answer': 'No worries, thanks for letting me know.',
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nI have to move our call to next week.\nOnly provide the reply.',
                'answer': 'No problem, next week works for me.',
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nI cannot attend the session today.\nOnly provide the reply.',
                'answer': 'No worries, thanks for telling me.',
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nCan we postpone lunch?\nOnly provide the reply.',
                'answer': 'Sure, we can do lunch another time.',
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nI need to leave early today.\nOnly provide the reply.',
                'answer': 'No problem, thanks for letting me know.',
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nI cannot join the call anymore.\nOnly provide the reply.',
                'answer': 'No worries, we can catch up later.',
            },
            {
                'prompt': 'Write a friendly reply as the recipient:\nCan we move dinner to another day?\nOnly provide the reply.',
                'answer': 'Sure, another day works for me.',
            },
            {
                'prompt': 'Write a kind reply as the recipient:\nI need to cancel because I am not feeling well.\nOnly provide the reply.',
                'answer': 'No problem, I hope you feel better soon.',
            },
        ],
    },

    'request_ack': {
        'examples': [
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nCan you send me the notes later?\nOnly provide the reply.',
                'answer': 'Sure, I can send them later.',
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nCan you check this when you have time?\nOnly provide the reply.',
                'answer': 'Of course, I will take a look when I can.',
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nCan you review my draft?\nOnly provide the reply.',
                'answer': 'Sure, I can review it.',
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nCan you remind me tomorrow?\nOnly provide the reply.',
                'answer': 'Sure, I can remind you tomorrow.',
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nCan you share the link with me?\nOnly provide the reply.',
                'answer': 'Sure, I will send you the link.',
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nCan you help me with this later?\nOnly provide the reply.',
                'answer': 'Of course, I can help later.',
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nCan you look over the slides?\nOnly provide the reply.',
                'answer': 'Sure, I can look over the slides.',
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nCan you send the agenda before the meeting?\nOnly provide the reply.',
                'answer': 'Sure, I will send the agenda before the meeting.',
            },
            {
                'prompt': 'Write a friendly reply as the recipient:\nCan you let me know when you arrive?\nOnly provide the reply.',
                'answer': 'Sure, I will let you know when I arrive.',
            },
            {
                'prompt': 'Write a friendly reply as the recipient:\nCan you take a look at this bug?\nOnly provide the reply.',
                'answer': 'Sure, I can take a look at the bug.',
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nCan you explain this part again?\nOnly provide the reply.',
                'answer': 'Of course, I can explain it again.',
            },
            {
                'prompt': 'Draft a friendly text message reply as the recipient:\nCan you send me the address?\nOnly provide the reply.',
                'answer': 'Sure, I will send you the address.',
            },
        ],
    },
}
