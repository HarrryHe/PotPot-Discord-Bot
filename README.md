async def announce_animal(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            #wait till the midnight to start this mission
            now = datetime.datetime.now()
            next_midnight = now.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
            wait_time = (next_midnight - now).total_seconds()
            await asyncio.sleep(wait_time)

            time_intervals = []
            #cut the 24hrs into 10 periods
            time_period = 24 * 60 * 60 // 10
            #so we are planning to announce the animal escaping announcement 10 times a day randomly
            #generated random time in each period
            for i in range(10):
                start = i * time_period
                end = (i+1) * time_period - 1
                time_intervals.append(random.randint(start, end))
            time_intervals.sort()

            #start interpret each announcement using for loop (total 10)
            for interval in time_intervals:
                now = datetime.datetime.now()
                target_time = now.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(seconds=interval)
                wait_time = (target_time - now).total_seconds()

                if wait_time < 0:
                    wait_time = 0
                await asyncio.sleep(wait_time)

                #initialization
                animal, points = self.select_animal()
                self.guild_tasks = {'animal': animal, 'points': points, 'time': datetime.datetime.now()}
                #make sure to clear all the users in the set that catches last animal
                self.caught_user.clear()

                #in each guilds
                for guild in self.bot.guilds:
                    config = load_guild_config(guild.id)
                    quest_channel_id = config.get('quest_channel')
                    if quest_channel_id:
                        channel = self.bot.get_channel(quest_channel_id)
                        if channel:
                            await channel.send(f"An animal has escaped! It's a {animal}. Type \'-catch\' to catch it and earn {points} points! You have 30 minutes to catch it.")