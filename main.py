
import importlib
import logging
import leczair
import classes


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
        # Beware though that this (and any other code touching classes)
        # can crash specacularly after a reload if the classes code is broken.
        # Such a crash will cause the bot to die completely. Therefore I
        # suggest only issuing a restart if you are around to deal with
        # Problems.
        state = classes.State.from_dict(state_dict)
        state.settings = leczair.load_settings()

        action = leczair.run_bot(state)

        # Serialise state for next iteration
        state_dict = dict(state)

        if action == 'restart':
            # Reload all modules (including the core modules)
            leczair.reload_modules()
            leczair.reload_modules([classes, leczair])


if __name__ == '__main__':
    main()

