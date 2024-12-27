# Web Development Module

## Final task

Develop a web application to visualize registered courses (University subjects) and analyze their difficulties.

Requirements:
- It should contain a dashboard with some metrics and graphs that provides insight about one course's difficulty;
- One could apply filters in the dashboard to visualize it by different undergraduate programs and semesters;
- It should contain another page for database administration that allows all CRUD funcionalities (Create, Retrieve, Update and Delete) for the tables. So one is able to visualize all registered information, edit and delete it, and add more;
- Develop back-end using Django REST Framework and front-end using React (JS or TS).

Tips:
- Calculate metrics such as average grade and failure rate. For that, you can create an "Enrollment" table in your database that registers every student subscription on each taken course, with their achieved grade;
- Use packages such as Material-UI and ApexCharts to improve your front-end appearence, as well as Axios to communicate with the API;
- Search on Django QuerySet documentation to improve your ViewSets. This way you will be able to run server-sided calculations instead of client-side, potentially optimizing your application.

## Example of solution

Checkout to branch ```final-project-example``` to see an intended solution for this case.

## References

- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [O Mapa do Django (PT-BR)](https://www.youtube.com/watch?v=-nTJz0dA7As)
- [Django QuerySet API reference](https://docs.djangoproject.com/en/5.1/ref/models/querysets/)
- [React Documentation](https://reactjs.org/docs/getting-started.html)
- [ApexCharts.js Documentation](https://apexcharts.com/)
- [Material-UI Documentation](https://mui.com/getting-started/usage/)
- [Axios Documentation](https://axios-http.com/docs/intro)