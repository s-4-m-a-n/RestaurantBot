# RestaurantBot 🤖💬

> Your Personal Food Ordering Assistant

The OrderEats Bot is a proof of concept project powered by Rasa that aims to provide a seamless food ordering experience. With advanced natural language processing capabilities, it allows users to effortlessly place food orders, track their status, and receive personalized recommendations based on their preferences.

## Features

- Intuitive conversational interface for placing orders :white_check_mark:
- Real-time order tracking and updates :white_check_mark:
- Personalized recommendations based on user preferences :black_square_button:
- Multi-platform support (web, mobile, messaging apps) :black_square_button:
- Integration with popular food delivery services :black_square_button:

## How to run

**1. Clone the repository:**

```bash
git@github.com:s-4-m-a-n/RestaurantBot.git
```

**2. Docker compose**

*:heavy_exclamation_mark: Make sure you have docker and docker compose installed on your system*
```bash
$ sudo docker compose up --build
```

**4. Train the model manually**
   - **get inside rasa-server container**
    ```bash
    $ docker exec -it rasa-server sh
    ```
    - **train rasa model**
    ```bash
    $ rasa train --fixed-model-name mymodel
    ```
## Endpoints
once the docker compose is up you can visit the following link to check out the chatbot

- `http://localhost:5000/chat`
- `http://localhost:5000/`

## Usage
- Interact with the ResBot through the chatbot web interface.
- Follow the prompts to place food orders, track their status, and explore personalized recommendations.

## Screenshots


## Contributing
Contributions are welcome! If you'd like to contribute to the OrderEats Bot project, please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your changes to your fork.
5. Submit a pull request.

## Acknowledgements

We would like to express our gratitude to the open-source community for providing the necessary tools and resources to develop this project.

## Contact
**For any inquiries or feedback, please reach out to us at `dhakalsumn739@gmail.com`.**

