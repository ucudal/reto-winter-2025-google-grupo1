from chat.bot import Bot
from chat.clients import create_bq_client, create_google_client
from chat.memory import get_path
from chat.tools.toolset import main_toolset
from chat.types import Dependencies
from env import Environment, env
from repository.conversation import ConversationRepository
from repository.types import ConversationModel, UserModel
from repository.user import UserRepository


class BotFactory:
    def default(self) -> Bot:
        return self.from_env(env())

    def from_env(self, env: Environment) -> Bot:
        deps = self.get_default_dependencies(env)
        return Bot(deps=deps, toolset=main_toolset)

    def get_default_dependencies(self, env: Environment):
        match env.memory:
            case "bigquery":
                bq_client = create_bq_client(env.project_id)

                user_repo = UserRepository(bq_client, env.project_id, env.dataset)
                user = user_repo.read(env.user_id)

                if user is None:
                    user_id = user_repo.create()
                    user = UserModel(user_id=user_id)

                conversation_repo = ConversationRepository(bq_client, env.project_id, env.dataset)
                conversation = conversation_repo.read(env.conversation_id)

                if conversation is None:
                    _ = conversation_repo.create(user.user_id, conversation_id=env.conversation_id)
                    conversation = ConversationModel(
                        conversation_id=env.conversation_id,
                        user_id=user.user_id,
                    )

            case "local":
                user = UserModel(user_id=env.user_id)

                path = get_path(user.user_id, env.conversation_id)

                if not path.is_file():
                    conversation = ConversationModel(
                        conversation_id=env.conversation_id,
                        user_id=user.user_id,
                    )

                    _ = get_path(user.user_id, conversation.conversation_id).write_text(
                        conversation.model_dump_json()
                    )
                else:
                    conversation = ConversationModel.model_validate_json(path.read_text())

        return Dependencies(
            env=env,
            bq_client=create_bq_client(env.project_id),
            google_client=create_google_client(env.google_cloud_api_key).aio,
            quotes=[],
            user=user,
            conversation=conversation,
        )
