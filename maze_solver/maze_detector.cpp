#include <iostream>
#include <string>
#include <vector>
#include <numeric>
#include <cmath>
#include <fstream>
#include <tuple>
#include <queue>

#include "image.h"
using namespace ComputerVisionProjects;

int apply_sobel_horizontal(Image *an_image, int x, int y){
    if (x < 1 || x >= an_image->num_rows()-1 || y < 1 || y >= an_image->num_columns()-1) {
      return 0;
    }
    int a = an_image->GetPixel(x-1, y-1) *  -1;
    int c = an_image->GetPixel(x+1, y-1) *   1;
    int d = an_image->GetPixel(x-1, y) *    -2;
    int f = an_image->GetPixel(x+1, y) *     2;
    int g = an_image->GetPixel(x-1, y+1) *  -1;
    int i = an_image->GetPixel(x+1, y+1)  *  1;
  
    return a + c + d + f + g + i;
}

int apply_sobel_vertical(Image *an_image, int x, int y){
    if (x < 1 || x >= an_image->num_rows()-1 || y < 1 || y >= an_image->num_columns()-1) {
        return 0;
    }
    int a = an_image->GetPixel(x-1, y-1) * 1;
    int b = an_image->GetPixel(x, y-1) * 2;
    int c = an_image->GetPixel(x+1, y-1) * 1;
    int g = an_image->GetPixel(x-1, y+1) * -1;
    int h = an_image->GetPixel(x, y+1) * -2;
    int i = an_image->GetPixel(x+1, y+1) * -1;

    return a + b + c + g + h + i;
}
void draw_bfs_path(Image* an_image, const std::vector<std::tuple<int, int>>& path) {
    for (size_t i = 1; i < path.size(); ++i) {

        auto [x1, y1] = path[i - 1];
        auto [x2, y2] = path[i];
        
        DrawLine(x1, y1, x2, y2, 0, an_image);
    }
}
std::vector<std::tuple<int, int>> reconstruct_path(std::vector<std::vector<std::tuple<int, int>>> parent, std::tuple<int, int> current, std::tuple<int, int> start, std::tuple<int, int> end){
    std::vector<std::tuple<int, int>> path;
    current = end;
    while (current != start){
        path.push_back(current);
        current = parent[std::get<0>(current)][std::get<1>(current)];
    }
    path.push_back(start);
    return path;
    
}
void apply_bfs(Image *binary_image, Image *original_image, int start_x, int start_y, int end_x, int end_y){
    //1227 660, 642 400 -> bluemousegray
    // int start_y = 330; int start_x = 577; -> mousegray
    // int end_y = 1242; int end_x = 45;

    std::cout << "Start pixel value: " << binary_image->GetPixel(start_x, start_y) << "\n";
    std::cout << "End pixel value: " << binary_image->GetPixel(end_x, end_y) << "\n";

    std::queue<std::tuple<int, int>> q;
    std::vector<std::vector<int>> visited{binary_image->num_rows(), std::vector<int>(binary_image->num_columns(), 0)};
    std::vector<std::vector<std::tuple<int, int>>> parent(
        binary_image->num_rows(),
        std::vector<std::tuple<int, int>>(binary_image->num_columns(), std::make_tuple(-1, -1))
    );
    q.push(std::make_tuple(start_x, start_y));
    visited[start_x][start_y]=1;
    std::vector<std::tuple<int, int>> directions = {std::make_tuple(0, 1),
        std::make_tuple(1, 0),
        std::make_tuple(0, -1),
        std::make_tuple(-1, 0)
    };
    while(!q.empty()){
        std::tuple<int, int> current = q.front();
        q.pop();
        if(std::get<0>(current) == end_x && std::get<1>(current) == end_y){
            auto path = reconstruct_path(parent, current, std::make_tuple(start_x, start_y), std::make_tuple(end_x, end_y));
            draw_bfs_path(original_image, path);
            return;
        }
        for(auto i : directions){
            auto neighbor = std::make_tuple(std::get<0>(current)+ std::get<0>(i), std::get<1>(current)+ std::get<1>(i));
            int nx = std::get<0>(neighbor);
            int ny = std::get<1>(neighbor);
            if (nx >= 0 && ny >= 0 && nx < binary_image->num_rows() && ny < binary_image->num_columns()) {
            
                if(binary_image->GetPixel(nx, ny) == 0 && visited[nx][ny] == 0){
                    visited[nx][ny] = 1;
                    parent[nx][ny] = current;
                    q.push(neighbor);
                }
            }
        }
    }
}
bool maze_detector(const std::string input_file, const std::string output_bfs_image_name, const std::string output_binary_image, int threshold, int start_x, int start_y, int end_x, int end_y){
    Image *an_image = new Image();
    ReadImage(input_file, an_image);
    Image output_image = *an_image;

    int gx, gy = 0;
    for(int i = 0; i< an_image->num_rows(); ++i){
        for (int j = 0; j< an_image->num_columns();++j){
            gx = apply_sobel_horizontal(an_image, i, j);
            gy = apply_sobel_vertical(an_image, i , j);
            int magnitude = sqrt((std::pow(gx, 2))+(std::pow(gy, 2)));
            output_image.SetPixel(i, j, magnitude);
        }
    }
    
    for (int i = 0; i < output_image.num_rows(); ++i){
        for (int j = 0; j < output_image.num_columns(); ++j){
        if(output_image.GetPixel(i,j) <= threshold){
            output_image.SetPixel(i,j,0);
        }
        else if (output_image.GetPixel(i,j) > threshold){
            output_image.SetPixel(i,j,255);
        }
        }
    }
    
    apply_bfs(&output_image, an_image, start_x, start_y, end_x, end_y);
    WriteImage(output_binary_image, output_image);
    WriteImage(output_bfs_image_name, *an_image);
    delete an_image;
    return true;
}
int main(int argc, char **argv){
  if (argc != 9) {
    std::cout << "Usage: " <<
      argv[0] << " {input_image_name} {output_bfs_image_name} {output_binary_image} {threshold} " << std::endl;
    return 0;
  }
  const std::string input_file(argv[1]);
  const std::string output_bfs_image_name(argv[2]);
  const std::string output_binary_image(argv[3]);
  int threshold = std::stoi(argv[4]);
  int start_x = std::stoi(argv[5]);
  int start_y = std::stoi(argv[6]);
  int end_x = std::stoi(argv[7]);
  int end_y = std::stoi(argv[8]);

  std::cout << "Running p1 " << input_file << " " 
         << output_bfs_image_name<<" "<<output_binary_image << std::endl;
  
  bool worked = maze_detector(input_file, output_bfs_image_name, output_binary_image, threshold, start_x, start_y, end_x, end_y);
  std::cout<< (worked ? "1": "0");

  return worked;
}
