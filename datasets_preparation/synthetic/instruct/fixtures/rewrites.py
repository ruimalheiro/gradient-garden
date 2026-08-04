_REDUNDANCY_REMOVAL_TEMPLATES = ['Rewrite this sentence to remove repeated meaning:\n'
 '{bad}\n'
 'Only provide the rewritten sentence.',
 'Remove redundant wording from this sentence:\n'
 '{bad}\n'
 'Return only the revised sentence.',
 'Rewrite the sentence without repeating the same idea:\n'
 '{bad}\n'
 'Do not explain your answer.',
 'Make this sentence non-redundant while preserving its meaning:\n'
 '{bad}\n'
 'Only output the rewrite.',
 'Delete the unnecessary repetition in this sentence:\n'
 '{bad}\n'
 'Provide one revised sentence only.',
 'Tighten this sentence by removing duplicated meaning:\n'
 '{bad}\n'
 'Answer with the corrected sentence and nothing else.',
 'Revise this sentence so each idea is stated once:\n{bad}\nOnly provide the revision.',
 'Replace this repetitive sentence with a clean version:\n'
 '{bad}\n'
 'Output only the replacement sentence.']

_REDUNDANCY_REMOVAL_EXAMPLES = [('The result was unclear because it was not clear.', 'The result was unclear.'),
 ('The plan failed because it did not work.', 'The plan was unsuccessful.'),
 ('The answer was wrong because it was not correct.', 'The answer was incorrect.'),
 ('The room was cold because it was not warm.', 'The room was cold.'),
 ('The task was easy because it was not hard.', 'The task was easy.'),
 ('The test was hard because it was difficult.', 'The test was difficult.'),
 ('The meeting was long because it took a lot of time.', 'The meeting was long.'),
 ('The food was good because it tasted nice.', 'The food tasted good.'),
 ('The movie was bad because it was not enjoyable.', 'The movie was bad.'),
 ('The instructions were confusing because they were hard to understand.',
  'The instructions were confusing.'),
 ('The device broke because it stopped working.', 'The device stopped working.'),
 ('The train was late because it arrived after the expected time.',
  'The train arrived late.'),
 ('The message was unclear because it was hard to understand.',
  'The message was unclear.'),
 ('The road was unsafe because it was dangerous.', 'The road was dangerous.'),
 ('The story was funny because it made people laugh.', 'The story was funny.'),
 ('She returned back to the office after lunch.',
  'She returned to the office after lunch.'),
 ('We planned ahead in advance for the conference.',
  'We planned ahead for the conference.'),
 ('Each individual participant received a badge.',
  'Each participant received a badge.'),
 ('The two teams collaborated together on the proposal.',
  'The two teams collaborated on the proposal.'),
 ('The committee reached a completely unanimous decision.',
  'The committee reached a unanimous decision.'),
 ('The end result surprised the researchers.', 'The result surprised the researchers.'),
 ('Please repeat the instructions again.', 'Please repeat the instructions.'),
 ('The pharmacy is located in close proximity to the station.',
  'The pharmacy is near the station.'),
 ('The customer received a free gift with the order.',
  'The customer received a gift with the order.'),
 ('Both versions contain the exact same data.', 'Both versions contain the same data.'),
 ('The workshop covered the basic fundamentals of budgeting.',
  'The workshop covered the fundamentals of budgeting.'),
 ('The company introduced a new innovation in battery design.',
  'The company introduced an innovation in battery design.'),
 ('The concert first began at eight o’clock.', 'The concert began at eight o’clock.'),
 ('In my personal opinion, the second option is clearer.',
  'In my opinion, the second option is clearer.'),
 ('A passport is a necessary requirement for this trip.',
  'A passport is required for this trip.'),
 ('The paths joined together near the river.', 'The paths joined near the river.'),
 ('The article reported a true fact about the experiment.',
  'The article reported a fact about the experiment.'),
 ('They postponed the discussion until later.', 'They postponed the discussion.'),
 ('The software reverted back to the earlier version.',
  'The software reverted to the earlier version.'),
 ('The cabin was surrounded on all sides by trees.',
  'The cabin was surrounded by trees.'),
 ('The unexpected surprise delighted the guests.',
  'The surprise delighted the guests.'),
 ('Her past history explains her interest in medicine.',
  'Her history explains her interest in medicine.'),
 ('Our future plans include opening a second office.',
  'Our plans include opening a second office.'),
 ('The speaker gave a brief summary in a few words.',
  'The speaker gave a brief summary.'),
 ('The final conclusion was supported by the evidence.',
  'The conclusion was supported by the evidence.')]

_CONCISE_REWRITE_TEMPLATES = ['Make this sentence more concise:\n{bad}\nOnly provide the revised sentence.',
 'Rewrite this sentence to be shorter:\n{bad}\nOnly provide the rewritten sentence.',
 'Make the following sentence less wordy:\n{bad}\nOnly output the revised sentence.',
 'Rewrite this sentence in fewer words:\n{bad}\nDo not explain your answer.',
 'Replace this sentence with a concise version:\n'
 '{bad}\n'
 'Only provide the replacement sentence.',
 'Shorten this sentence without losing any important meaning:\n'
 '{bad}\n'
 'Return only the rewrite.',
 'Edit this sentence for brevity:\n'
 '{bad}\n'
 'Provide one concise sentence and nothing else.']

_CONCISE_REWRITE_EXAMPLES = [('Due to the fact that it was raining, we decided not to go outside.',
  'Because it was raining, we did not go outside.'),
 ('At this point in time, we are ready to begin.', 'We are ready to begin now.'),
 ('The reason I was late was because I arrived after the time.', 'I arrived late.'),
 ('The reason we left was because we needed to go.', 'We needed to leave.'),
 ('She gave a reply after a short amount of time.', 'She replied quickly.'),
 ('The train arrived later than the time it was supposed to arrive.',
  'The train arrived late.'),
 ('He was not able to find his keys.', 'He could not find his keys.'),
 ('The shop is open during the hours of the morning.',
  'The shop is open in the morning.'),
 ('The project was completed before the time it was due.',
  'The project was completed before the deadline.'),
 ('She fixed the mistake that was in the document.',
  'She corrected the mistake in the document.'),
 ('The computer was slow and took a long time to respond.',
  'The computer responded slowly.'),
 ('The bag was heavy because it had many books inside.',
  'The bag was heavy with books.'),
 ('He used his phone to send a message to his friend.', 'He texted his friend.'),
 ('The water was too hot to drink right away.',
  'The water needed to cool before drinking.'),
 ('The city has many buildings that are very tall.',
  'The city has many tall buildings.'),
 ('The cake tasted sweet and was nice to eat.', 'The cake was sweet and delicious.'),
 ('The task was easy and did not take much effort.', 'The task was easy.'),
 ('The message was not clear and could be misunderstood.', 'The message was unclear.'),
 ('She looked at the paper carefully to find mistakes.',
  'She reviewed the paper for mistakes.'),
 ('The phone stopped working and would not turn on.', 'The phone would not turn on.'),
 ('During the course of the meeting, we reviewed the budget.',
  'During the meeting, we reviewed the budget.'),
 ('We changed the schedule in order to avoid a conflict.',
  'We changed the schedule to avoid a conflict.'),
 ('A large number of customers requested refunds.',
  'Many customers requested refunds.'),
 ('This device has the ability to record audio.', 'This device can record audio.'),
 ('She checks the inventory on a daily basis.', 'She checks the inventory daily.'),
 ('The team made the decision to delay the launch.',
  'The team decided to delay the launch.'),
 ('He opened the window for the purpose of cooling the room.',
  'He opened the window to cool the room.'),
 ('In the event that the bus is late, call me.', 'If the bus is late, call me.'),
 ('We can discuss the details at a later point in time.',
  'We can discuss the details later.'),
 ('Despite the fact that she was tired, she finished the report.',
  'Although she was tired, she finished the report.'),
 ('The guide provided an explanation of the safety rules.',
  'The guide explained the safety rules.'),
 ('The technician conducted an investigation into the fault.',
  'The technician investigated the fault.'),
 ('After reviewing the evidence, they came to the conclusion that the claim was false.',
  'After reviewing the evidence, they concluded that the claim was false.'),
 ('Mina has a preference for working in the morning.',
  'Mina prefers working in the morning.'),
 ('He made an attempt to restart the printer.', 'He tried to restart the printer.'),
 ('I have a question with regard to the invoice.',
  'I have a question about the invoice.'),
 ('There are three reasons why the proposal should be revised.',
  'Three reasons support revising the proposal.'),
 ('The flight was canceled because of the fact that the runway was icy.',
  'The flight was canceled because the runway was icy.'),
 ('The majority of the files were already backed up.',
  'Most files were already backed up.'),
 ('Nora was responsible for managing the guest list.', 'Nora managed the guest list.'),
 ('The reviewer made a recommendation that we shorten the introduction.',
  'The reviewer recommended shortening the introduction.'),
 ('We gave consideration to several possible routes.', 'We considered several routes.'),
 ('Jon has knowledge of the local regulations.', 'Jon knows the local regulations.'),
 ('The courier was in possession of the package.', 'The courier had the package.'),
 ('The meeting that is scheduled for tomorrow has been moved online.',
  'Tomorrow’s meeting has moved online.'),
 ('The report that was written by Maya identifies two risks.',
  'Maya’s report identifies two risks.'),
 ('The files that are located in the archive can be deleted.',
  'The archived files can be deleted.'),
 ('We should make use of the quieter room.', 'We should use the quieter room.')]

_NATURAL_PARAPHRASE_TEMPLATES = ['Rewrite this sentence so it sounds more natural:\n'
 '{bad}\n'
 'Only provide the rewritten sentence.',
 'Make this sentence sound natural:\n{bad}\nOnly provide the improved sentence.',
 'Rewrite the following sentence naturally:\n{bad}\nDo not explain your answer.',
 'Improve the wording of this sentence:\n{bad}\nOnly output the improved sentence.',
 'Rewrite this sentence in a natural way:\n{bad}\nOnly provide the rewritten sentence.',
 'Make this wording fluent and idiomatic:\n{bad}\nReturn only the revised sentence.',
 'Replace the awkward wording with a natural sentence:\n'
 '{bad}\n'
 'Provide only the replacement.']

_NATURAL_PARAPHRASE_EXAMPLES = [('I am writing to tell you that I am happy about the thing.', 'I am happy about it.'),
 ('I want to say that the book was something I liked.', 'I liked the book.'),
 ('The thing was bad because it was not good.', 'The item was of poor quality.'),
 ('He went to the place where the thing happened.', 'He went to the scene.'),
 ('The food was nice and I liked it a lot.', 'I really enjoyed the food.'),
 ('This is a thing that people use to do work.', 'This is a tool people use for work.'),
 ('She was happy because the result was good.', 'She was pleased with the result.'),
 ('He said the same thing again and again many times.',
  'He repeated himself many times.'),
 ('I need help with the problem that I am having.', 'I need help with my problem.'),
 ('The movie was interesting and kept my attention.', 'The movie was engaging.'),
 ('She spoke in a way that was easy to understand.', 'She spoke clearly.'),
 ('The house was big and had a lot of space.', 'The house was spacious.'),
 ('The dog ran fast across the field.', 'The dog sprinted across the field.'),
 ('The teacher explained the idea in a simple way.',
  'The teacher explained the idea simply.'),
 ('The river moved slowly through the valley.',
  'The river flowed slowly through the valley.'),
 ('The idea was new and different from the usual ideas.', 'The idea was original.'),
 ('The report includes details about what happened.',
  'The report describes what happened.'),
 ('She was kind and helped the person who needed help.',
  'She kindly helped the person in need.'),
 ('He asked a question that was important.', 'He asked an important question.'),
 ('They worked together to solve the problem.',
  'They collaborated to solve the problem.'),
 ('Could you maybe possibly send me the updated schedule?',
  'Could you send me the updated schedule?'),
 ('The bus made its arrival ten minutes late.', 'The bus arrived ten minutes late.'),
 ('She did a quick check of the numbers before submitting them.',
  'She quickly checked the numbers before submitting them.'),
 ('I am not sure what it is that you mean.', 'I am not sure what you mean.'),
 ('The room has not enough chairs for everyone.',
  'The room does not have enough chairs for everyone.'),
 ('He explained me the process after the meeting.',
  'He explained the process to me after the meeting.'),
 ('We discussed about the new schedule yesterday.',
  'We discussed the new schedule yesterday.'),
 ('Please revert back to me when you have an answer.',
  'Please reply when you have an answer.'),
 ('We need to make the meeting at nine tomorrow.',
  'We need to hold the meeting at nine tomorrow.'),
 ('The package reached to my house this morning.',
  'The package arrived at my house this morning.'),
 ('She is working here since March.', 'She has worked here since March.'),
 ('Can you explain me how this setting works?',
  'Can you explain how this setting works?'),
 ('My phone battery became empty during the trip.',
  'My phone battery died during the trip.'),
 ('The coffee has a very strong taste today.', 'The coffee tastes very strong today.'),
 ('The road was having heavy traffic after the concert.',
  'Traffic was heavy on the road after the concert.'),
 ('After the report was finished, it was sent to the client.',
  'Once finished, the report was sent to the client.'),
 ('I am looking forward to meet the new team.',
  'I am looking forward to meeting the new team.'),
 ('There is no need for you to worry about the delay.',
  'You do not need to worry about the delay.'),
 ('The store remains close on Sundays.', 'The store remains closed on Sundays.'),
 ('He gave to me the receipt before leaving.',
  'He gave me the receipt before leaving.'),
 ('We reached to the station just before noon.',
  'We reached the station just before noon.'),
 ('This solution is more better than the first one.',
  'This solution is better than the first one.'),
 ('The team discussed on the budget for an hour.',
  'The team discussed the budget for an hour.'),
 ('She suggested me to take an earlier train.',
  'She suggested that I take an earlier train.'),
 ('The weather became worse as we approached the coast.',
  'The weather worsened as we approached the coast.'),
 ('The instructions say us to restart the device.',
  'The instructions tell us to restart the device.'),
 ('I made a photo of the damaged package.', 'I took a photo of the damaged package.'),
 ('The train was with a delay of twenty minutes.',
  'The train was delayed by twenty minutes.')]

_HIGH_EDIT_DISTANCE_TEMPLATES = ['Rewrite this sentence. Do not copy the original wording:\n'
 '{bad}\n'
 'Only provide the rewritten sentence.',
 'Paraphrase this sentence with different wording:\n'
 '{bad}\n'
 'Only provide the paraphrase.',
 'Rewrite this sentence using a different structure:\n'
 '{bad}\n'
 'Only output the rewritten sentence.',
 'Replace this sentence with a clearer version that uses different wording:\n'
 '{bad}\n'
 'Only provide the replacement sentence.',
 'Rewrite the sentence below without copying its phrasing:\n'
 '{bad}\n'
 'Only provide the rewritten sentence.',
 'Express the same meaning with substantially different wording:\n'
 '{bad}\n'
 'Return one sentence only.',
 'Restructure and rephrase this sentence while preserving every fact:\n'
 '{bad}\n'
 'Output only the rewrite.',
 'Write a high-edit-distance paraphrase of this sentence:\n'
 '{bad}\n'
 'Do not add an explanation.']

_HIGH_EDIT_DISTANCE_EXAMPLES = [('The issue happened because there was a problem with the system.',
  'A system fault caused the incident.'),
 ('The device stopped working because it had an issue.',
  'A fault rendered the device inoperable.'),
 ('The weather was bad because it rained all day.',
  'A full day of rain created unpleasant conditions.'),
 ('The child was scared because the noise was loud.',
  'The volume of the noise frightened the child.'),
 ('He was tired because he did not sleep enough.',
  'Insufficient sleep left him fatigued.'),
 ('The path was hard to see because it was dark.', 'Darkness obscured the route.'),
 ('The company made changes to make the product better.',
  'The firm pursued improvements by revising its product.'),
 ('The book was about a person who went on a trip.',
  'A traveler’s journey is the focus of the book.'),
 ('The car made a loud sound when it started.',
  'Starting the car produced a loud noise.'),
 ('She gave me information that was useful.', 'What she told me proved valuable.'),
 ('He made a decision very quickly without thinking much.',
  'His rushed choice lacked deliberation.'),
 ('The room was very cold and not warm at all.', 'The room felt freezing.'),
 ('The game was fun and made people excited.',
  'People found the game both thrilling and entertaining.'),
 ('The instructions were confusing and hard to understand.',
  'The directions lacked clarity.'),
 ('The answer was not correct and had mistakes.', 'Errors made the answer inaccurate.'),
 ('The meeting was long and it took a lot of time.', 'The meeting dragged on.'),
 ('The plan did not work because it failed.', 'The plan proved unsuccessful.'),
 ('The test was hard and difficult to finish.',
  'Completing the exam proved demanding.'),
 ('The food was good because it tasted nice.', 'The meal had a delicious flavor.'),
 ('The project was not finished because the team needed more time.',
  'Insufficient time kept the team from completing the project.'),
 ('Maria put the keys by the door so she would remember them in the morning.',
  'To avoid forgetting her keys the next morning, Maria left them beside the door.'),
 ('The manager postponed the launch after testing revealed a serious bug.',
  'A serious bug found during testing forced the manager to delay the launch.'),
 ('Since the café was full, we took our drinks to the park.',
  'With no seats available at the café, we carried our drinks to the park.'),
 ('Ravi checked every figure before sending the report to the client.',
  'Before emailing the report to the client, Ravi verified all the figures.'),
 ('The storm damaged the bridge, so drivers had to use another road.',
  'Drivers took a detour after the storm left the bridge unusable.'),
 ('Lena lowered the music because her neighbor was trying to sleep.',
  'Knowing her neighbor needed rest, Lena turned the music down.'),
 ('The library extended its hours during exams to give students more study time.',
  'Students gained extra study time when the library stayed open later for exams.'),
 ('The package arrived late even though the seller shipped it on time.',
  'Despite timely dispatch by the seller, the delivery was delayed.'),
 ('I wrote down the address because I did not want to forget it.',
  'To make sure I remembered the address, I recorded it.'),
 ('The team simplified the form after users said it was confusing.',
  'User complaints about confusion prompted the team to redesign the form more '
  'simply.'),
 ('The hikers turned back when thick fog hid the trail.',
  'Unable to see the trail through the dense fog, the hikers returned the way they '
  'came.'),
 ('Nadia missed the call because her phone was on silent.',
  'With her phone muted, Nadia did not notice the call.'),
 ('The chef changed the recipe to make the soup less salty.',
  'To reduce the soup’s saltiness, the chef adjusted the recipe.'),
 ('The museum closed one gallery while workers repaired the ceiling.',
  'Ceiling repairs required the museum to shut a gallery temporarily.'),
 ('Owen took the earlier bus so he could arrive before the interview.',
  'To reach the interview in advance, Owen caught an earlier bus.'),
 ('The teacher extended the deadline because several students were ill.',
  'Several student illnesses led the teacher to allow more time.'),
 ('The battery lasted longer after I reduced the screen brightness.',
  'Lowering the display brightness extended the battery life.'),
 ('We moved the picnic indoors when the rain began.',
  'The start of the rain forced us to hold the picnic inside.'),
 ('The editor removed two paragraphs because they repeated earlier points.',
  'Two paragraphs were cut by the editor for duplicating ideas already stated.'),
 ('The shop refunded the payment after confirming that the item was defective.',
  'Once the defect was verified, the shop returned the customer’s money.')]

_VAGUE_REPAIR_TEMPLATES = ['Rewrite this sentence to be clearer:\n{bad}\nOnly provide the rewritten sentence.',
 'Rewrite this weak sentence directly:\n{bad}\nOnly provide the rewritten sentence.',
 'Replace this weak sentence with a clearer version:\n'
 '{bad}\n'
 'Only provide the replacement sentence.',
 'Rewrite this sentence to remove vague wording:\n'
 '{bad}\n'
 'Only output the rewritten sentence.',
 'Improve this sentence so it sounds natural:\n'
 '{bad}\n'
 'Only provide the improved sentence.',
 'Replace the vague judgment with a concise statement:\n'
 '{bad}\n'
 'Return only the revision.',
 'Rewrite this weak sentence using precise wording:\n'
 '{bad}\n'
 'Provide one revised sentence only.']

_VAGUE_REPAIR_EXAMPLES = [('The thing was bad because it was not good.', 'The item was unsatisfactory.'),
 ('The movie was bad because the plot did not make sense.',
  'The movie had an incoherent plot.'),
 ('The food was bad because it was cold and undercooked.',
  'The food was cold and undercooked.'),
 ('The answer was bad because it ignored the second part of the question.',
  'The answer omitted the question’s second part.'),
 ('The idea was bad because it required more money than we had.',
  'The idea exceeded the available budget.'),
 ('The design was bad because the labels were too small to read.',
  'The design used unreadably small labels.'),
 ('The result was bad because the test showed lower accuracy than the baseline.',
  'The test result fell below the baseline accuracy.'),
 ('The service was bad because the staff kept the customer waiting for an hour.',
  'The service left the customer waiting for an hour.'),
 ('The explanation was bad because it skipped the key step.',
  'The explanation omitted the key step.'),
 ('The performance was bad because the actor forgot several lines.',
  'Several forgotten lines disrupted the performance.'),
 ('The plan was bad because it named no owner or deadline.',
  'The plan lacked an owner and a deadline.'),
 ('The writing was bad because the paragraphs were not in a logical order.',
  'The paragraphs were arranged illogically.'),
 ('The app was bad because it crashed whenever I uploaded a photo.',
  'The app crashed whenever I uploaded a photo.'),
 ('The lesson was bad because its examples did not match the concept.',
  'The lesson used examples unrelated to the concept.'),
 ('The meeting was bad because it ended with no decision or action items.',
  'The meeting ended without a decision or action items.'),
 ('The tool was bad because its handle came loose during normal use.',
  'The tool’s handle loosened during normal use.'),
 ('The choice was bad because it doubled our travel time.',
  'The choice doubled our travel time.'),
 ('The experience was bad because the room was noisy all night.',
  'The noisy room made the night unpleasant.'),
 ('The code was bad because it duplicated the same logic in five places.',
  'The code repeated the same logic in five places.'),
 ('The response was bad because it never answered the question.',
  'The response did not answer the question.'),
 ('The schedule was bad because it was not planned well.',
  'The schedule was poorly organized.'),
 ('The interface was bad because it was hard to use.',
  'The interface was difficult to navigate.'),
 ('The route was bad because it took too long.', 'The route was inefficient.'),
 ('The instructions were bad because they did not explain the steps.',
  'The instructions omitted the necessary steps.'),
 ('The photo was bad because it was not clear.', 'The photo was blurry.'),
 ('The argument was bad because it did not have enough support.',
  'The argument lacked sufficient evidence.'),
 ('The repair was bad because the problem came back.',
  'The repair did not resolve the problem.'),
 ('The presentation was bad because people could not follow it.',
  'The presentation was difficult to follow.'),
 ('The search results were bad because they were not related to the question.',
  'The search results were irrelevant to the question.'),
 ('The estimate was bad because it was far from the actual cost.',
  'The estimate was inaccurate.'),
 ('The packaging was bad because the item arrived damaged.',
  'The packaging failed to protect the item.'),
 ('The translation was bad because it changed the meaning.',
  'The translation distorted the meaning.')]

REWRITE_FIXTURES = {
    'redundancy_removal': {
        'messages': [
            {
                'role': 'user',
                'content': list(_REDUNDANCY_REMOVAL_TEMPLATES),
            },
            {
                'role': 'assistant',
                'content': '{answer}',
            },
        ],
        'examples': [
            {
                'bad': bad,
                'answer': answer,
            }
            for bad, answer in _REDUNDANCY_REMOVAL_EXAMPLES
        ],
    },
    'concise_rewrite': {
        'messages': [
            {
                'role': 'user',
                'content': list(_CONCISE_REWRITE_TEMPLATES),
            },
            {
                'role': 'assistant',
                'content': '{answer}',
            },
        ],
        'examples': [
            {
                'bad': bad,
                'answer': answer,
            }
            for bad, answer in _CONCISE_REWRITE_EXAMPLES
        ],
    },
    'natural_paraphrase': {
        'messages': [
            {
                'role': 'user',
                'content': list(_NATURAL_PARAPHRASE_TEMPLATES),
            },
            {
                'role': 'assistant',
                'content': '{answer}',
            },
        ],
        'examples': [
            {
                'bad': bad,
                'answer': answer,
            }
            for bad, answer in _NATURAL_PARAPHRASE_EXAMPLES
        ],
    },
    'high_edit_distance': {
        'messages': [
            {
                'role': 'user',
                'content': list(_HIGH_EDIT_DISTANCE_TEMPLATES),
            },
            {
                'role': 'assistant',
                'content': '{answer}',
            },
        ],
        'examples': [
            {
                'bad': bad,
                'answer': answer,
            }
            for bad, answer in _HIGH_EDIT_DISTANCE_EXAMPLES
        ],
    },
    'bad_because_not_good': {
        'messages': [
            {
                'role': 'user',
                'content': list(_VAGUE_REPAIR_TEMPLATES),
            },
            {
                'role': 'assistant',
                'content': '{answer}',
            },
        ],
        'examples': [
            {
                'bad': bad,
                'answer': answer,
            }
            for bad, answer in _VAGUE_REPAIR_EXAMPLES
        ],
    },
}
