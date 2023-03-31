Learn how to crawling shopee.vn
# Overview
## Danh sách các function để lấy dữ liệu shopee
> 1. search_get_items
> 2. search_only_voucher
> 3. get_industry_data
> 4. get_facet
> 5. get_items_from_industry
> 6. get_in4_item
> 7. get_full_in4_item

## Chi tiết functions
### Xử lý dữ liệu: from data_process
- browser: Mở trình duyệt
- get_json_data: Lấy dữ liệu json từ queue
### Lấy dữ liệu shopee: from shopee_crawler
- search_get_items: Lấy items theo từ khóa tìm kiếm (e.g. link https://shopee.vn/search?keyword=b%E1%BB%89m%20youli)
- search_only_voucher: Từ danh sách theo từ khóa tìm kiếm, lọc dữ liệu có voucher
- get_industry_data: Lấy danh sách mã ID ngành hàng mẹ
- get_facet: Lấy danh sách mã ID ngành hàng con
- get_items_from_industry: Lấy items theo ngành hàng thay vì từ khóa tìm kiếm
- get_in4_item: Lấy thông tin chi tiết từng sản phẩm theo shopid và itemid
- get_full_in4_item: Lấy tất cả các trường thông tin từng sản phẩm
