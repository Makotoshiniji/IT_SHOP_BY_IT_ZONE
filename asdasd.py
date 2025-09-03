ctk.set_appearance_mode("light")  
        ctk.set_default_color_theme("blue")
        self.cart_items = []

        self.product_frame_container = ctk.CTkFrame(   display,
            width=1800, height=5000)
        self.product_frame_container.place( x=70,y=100)

        self.canvas = ctk.CTkCanvas(self.product_frame_container, highlightthickness=0, width=1700, height=850)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = ctk.CTkScrollbar(self.product_frame_container, command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollable_frame = ctk.CTkFrame(self.canvas, width=1800, height=5000)
        self.scrollable_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.load_products_from_db()


    def load_products_from_db(self):
        """Load product details without images."""
        try:
            self.cursor.execute("SELECT code, name, detail, price FROM products")
            products_list = [
                {"code": row[0],"name": row[1], "detail": row[2], "price": row[3]} for row in self.cursor.fetchall()
            ]
            self.display_products(products_list)
        except Exception as e:
            messagebox.showerror("Database Error", f"Error loading products: {e}")

    def get_image_from_db(self, product_id):
        """Load the image for a specific product."""
        try:
            self.cursor.execute("SELECT image FROM products WHERE id = ?", (product_id,))
            result = self.cursor.fetchone()
            if result:
                return result[0]  # Return the binary image data
        except Exception as e:
            print(f"Error fetching image for product {product_id}: {e}")
        return None

    def display_products(self, products_list):
        """Display product details in the UI."""
        for i, product in enumerate(products_list):
            self.add_product_to_frame(product, i)

    def add_product_to_frame(self, product, index):
        """Add a product's details and image (on demand) to a frame."""
        product_frame = ctk.CTkFrame(self.scrollable_frame, width=300, height=300, corner_radius=10)
        product_frame.grid(row=index // 4, column=index % 4, padx=10, pady=10)
        product_frame.pack_propagate(False)

        # Display product details

        # Load and display the image on demand
        try:
            img_data = self.get_image_from_db(product["image"])  # Fetch image blob from database
            if img_data:
                img_data = io.BytesIO(img_data)
                pil_image = Image.open(img_data).resize((10, 10))
                tk_img = ImageTk.PhotoImage(pil_image)
                img_label = ctk.CTkLabel(product_frame, image=tk_img, text="")
                img_label.image = tk_img  # Keep a reference to avoid garbage collection
                img_label.pack(pady=10)
            else:
                ctk.CTkLabel(product_frame, text="Image unavailable").pack(pady=5)
        except Exception as e:
            print(f"Image error: {e}")
            ctk.CTkLabel(product_frame, text="Image unavailable").pack(pady=5)
        
        ctk.CTkLabel(product_frame, text=f"{product['name']}\n{product['detail']}\n฿{product['price']}").pack(pady=5)


        # Add a button
        ctk.CTkButton(product_frame, text="Add", command=lambda: self.add_to_cart(product)).pack(pady=5)    
