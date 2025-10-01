from django.urls import reverse

class TestUrls:
    def test_dashboard_url(self):
        url = reverse('links:dashboard')
        assert url == '/'
    
    def test_my_page_url(self):
        url = reverse('links:my-page', args=['test'])
        assert url == '/my_page/test/'
    
    def test_link_list_url(self):
        url = reverse('links:link-list')
        assert url == '/link/list/'

    def test_link_detail_url(self):
        url = reverse('links:link-detail', args=[1])
        assert url == f'/link/detail/{1}/'
    
    def test_link_create_url(self):
        url = reverse('links:link-create')
        assert url == '/link/create/'
    
    def test_link_update_url(self):
        url = reverse('links:link-update', args=[1])
        assert url == f'/link/update/{1}/'

    def test_link_delete_url(self):
        url = reverse('links:link-delete', args=[1])
        assert url == f'/link/delete/{1}/'