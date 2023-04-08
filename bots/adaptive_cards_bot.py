# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import json
import os
import random
import requests
import pandas as pd
from botFuncs.basic import recognize_simple_message, ask_anything_flow

from botbuilder.core import ActivityHandler, TurnContext, CardFactory, MessageFactory
from botbuilder.schema import ChannelAccount, Attachment, Activity, ActivityTypes

CARDS = [
    # "resources/FlightItineraryCard.json",

    # "resources/LargeWeatherCard.json",
    # "resources/RestaurantCard.json",
    # "resources/SolitaireCard.json"
    "resources/ImageGalleryCard.json",
]


class AdaptiveCardsBot(ActivityHandler):
    """
    This bot will respond to the user's input with an Adaptive Card. Adaptive Cards are a way for developers to
    exchange card content in a common and consistent way. A simple open card format enables an ecosystem of shared
    tooling, seamless integration between apps, and native cross-platform performance on any device. For each user
    interaction, an instance of this class is created and the OnTurnAsync method is called.  This is a Transient
    lifetime service. Transient lifetime services are created each time they're requested. For each Activity
    received, a new instance of this class is created. Objects that are expensive to construct, or have a lifetime
    beyond the single turn, should be carefully managed.
    """

    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    f"Welcome to Adaptive Cards Bot  {member.name}. This bot will "
                    f"introduce you to Adaptive Cards. Type anything to see an Adaptive "
                    f"Card."
                )

    async def on_message_activity(self, turn_context: TurnContext):
        print("CONTEXT--", turn_context.activity)
        # print("LOGGER--", turn_context.activity)
        message = Activity(
            text="Here is an Adaptive Card:",
            type=ActivityTypes.message,
            attachments=[self._create_adaptive_card_attachment()],
        )
        response = requests.get("https://www.greetingsapi.com/random")
        json_data = response.json()
        print("LOGGER--", json_data['greeting'])

        if (str(turn_context.activity.text).__contains__("analyse")):
            return await turn_context.send_activity(MessageFactory.text("Sure, please send the data"))

        if turn_context.activity.attachments:
            return await turn_context.send_activity(MessageFactory.text("Average sales are 75 per day"))

        msg_type, resp = recognize_simple_message(turn_context.activity.text)

        if msg_type == "greeting" or msg_type == "leaving":
            return await turn_context.send_activity(MessageFactory.text(resp))

        if msg_type == "other":
            return await turn_context.send_activity(MessageFactory.text(ask_anything_flow(turn_context.activity.text)))

        await turn_context.send_activity(message)

    def _create_adaptive_card_attachment(self) -> Attachment:
        """
        Load a random adaptive card attachment from file.
        :return:
        """
        random_card_index = random.randint(0, len(CARDS) - 1)
        card_path = os.path.join(os.getcwd(), CARDS[random_card_index])
        with open(card_path, "rb") as in_file:
            card_data = json.load(in_file)

        return CardFactory.adaptive_card(card_data)


# ab ismein one more thing how can we introduce flows here
# convo flows ,, it will work just like topics
# what destination  check destination func me wo func select kr lo
# then check if that is okay for that function else check and then else
# check with that function select function ek selector flow ban sakta hai ispe
# ispe hamara ek selector flow ban sakta hai aur ab humare pas
# python hai to api calls aur sab kuch bhi possible hai
