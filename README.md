# Flowers Identification Website
A project to identify 102 different flower types. It uses a **Machine Learning** model that was trained on the `102 Category Flower Dataset`. The stack used is **FastAPI** for backend, **React** for frontend, **nginx** for server management, **docker** for containerization and **PyTorch** for CNN model training.

## Install
1. Install docker (if not already installed), refer to [this guide](https://docs.docker.com/get-docker/)
1. Clone this repo
   ```
   $ git clone <repo.git>
   ```
1. Build the project's containers
   ```
   $ cd <repo_name>
   $ docker-compose -f "docker-compose.yml" up -d --build
   ```
1. Launch a web browser and go to `localhost` or `127.0.0.1`

## Develop and Test
TODO

## Development Plan
- [x] Create containers
- [x] Build server
- [ ] Build UI
- [ ] Add training results

## References
```
@InProceedings{Nilsback08,
  author       = "Maria-Elena Nilsback and Andrew Zisserman",
  title        = "Automated Flower Classification over a Large Number of Classes",
  booktitle    = "Indian Conference on Computer Vision, Graphics and Image Processing",
  month        = "Dec",
  year         = "2008",
}
```