node {
    checkout scm

    /* Registry + credentials ID from jenkins */
    docker.withRegistry('https://registry.esav.fi', '2e7e1a1e-560a-4962-b3ce-12128f4c8d43') {

        def customImage = docker.build("projects/displaymanage:${env.BUILD_ID}")

        /* Push the container to the custom Registry */
        customImage.push()
        customImage.push('latest')
    }
}
