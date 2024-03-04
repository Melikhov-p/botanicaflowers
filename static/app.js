new Vue({
    el: '#products',
    data: {
        products: []
    },
    created() {
        axios
            .get('/api/product')
            .then(response => (this.products = response.data))
    }
})