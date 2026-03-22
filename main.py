from app import init_widgets


def main():
    init_widgets.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
