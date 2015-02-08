
import importlib
import logging
import leczair
import frozenstate


logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.DEBUG)
    state_dict = {}

    while True:
        # Base the state on the serialisation of the previous state. By
        # going through the serialisation we allow reloading of the state
        # module without accidentally messing something up because the
        # state object abstraction changed in the reload.
        # 
        # Beware though that this (and any other code touching frozenstate)
        # can crash specacularly after a reload if the frozenstate code is
        # broken. Such a crash will cause the bot to die completely. Therefore
        # I suggest only issuing a restart if you are around to deal with
        # Problems.
        settings = frozenstate.single('settings', leczair.load_settings())
        state = frozenstate.append(frozenstate.from_dict(state_dict), settings)

        action = leczair.run_bot(state)

        # Serialise state for next iteration
        state_dict = frozenstate.to_dict(state)

        if action == 'restart':
            # Reload all modules (including the core modules)
            leczair.reload_modules()
            leczair.reload_modules([frozenstate, leczair])


if __name__ == '__main__':
    main()

