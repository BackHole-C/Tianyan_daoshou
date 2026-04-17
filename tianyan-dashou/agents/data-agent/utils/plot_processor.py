#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
地块数据处理器
功能：加载地块边界数据、处理空间信息
"""

import json
import os
from shapely.geometry import shape, Polygon
from loguru import logger

class PlotProcessor:
    def __init__(self, config):
        """初始化地块处理器"""
        self.config = config
        self.source = config['source']
        self.geojson_path = config['geojson_path']
        self.field_mapping = config['field_mapping']
    
    def load_plots(self):
        """加载地块数据"""
        try:
            logger.info("加载地块数据")
            
            if self.source == 'geojson':
                plots = self._load_from_geojson()
            else:
                plots = self._load_from_database()
            
            logger.info(f"成功加载 {len(plots)} 个地块")
            return plots
            
        except Exception as e:
            logger.error(f"加载地块数据失败: {str(e)}")
            return []
    
    def _load_from_geojson(self):
        """从GeoJSON文件加载地块数据"""
        try:
            if os.path.exists(self.geojson_path):
                with open(self.geojson_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return data['features']
            else:
                # 如果文件不存在，生成模拟数据
                logger.warning(f"GeoJSON文件不存在: {self.geojson_path}")
                return self._generate_mock_plots()
        except Exception as e:
            logger.error(f"从GeoJSON加载失败: {str(e)}")
            return self._generate_mock_plots()
    
    def _load_from_database(self):
        """从数据库加载地块数据"""
        # 这里应该连接数据库查询，现在返回模拟数据
        return self._generate_mock_plots()
    
    def _generate_mock_plots(self):
        """生成模拟地块数据"""
        mock_plots = [
            {
                "type": "Feature",
                "properties": {
                    "plot_id": "PLOT_001",
                    "plot_name": "王大哥-示范田",
                    "area_mu": 50.5,
                    "crop_type": "rice",
                    "variety": "杂交稻",
                    "owner": "王大哥",
                    "phone": "13800138001"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [116.404, 39.915],
                        [116.414, 39.915],
                        [116.414, 39.925],
                        [116.404, 39.925],
                        [116.404, 39.915]
                    ]]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "plot_id": "PLOT_002",
                    "plot_name": "李大姐-试验田",
                    "area_mu": 30.0,
                    "crop_type": "rice",
                    "variety": "常规稻",
                    "owner": "李大姐",
                    "phone": "13900139002"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [116.414, 39.915],
                        [116.424, 39.915],
                        [116.424, 39.925],
                        [116.414, 39.925],
                        [116.414, 39.915]
                    ]]
                }
            }
        ]
        
        # 保存到文件
        mock_geojson = {
            "type": "FeatureCollection",
            "features": mock_plots
        }
        
        os.makedirs(os.path.dirname(self.geojson_path), exist_ok=True)
        with open(self.geojson_path, 'w', encoding='utf-8') as f:
            json.dump(mock_geojson, f, ensure_ascii=False, indent=2)
        
        logger.info(f"生成模拟地块数据并保存到: {self.geojson_path}")
        return mock_plots
    
    def get_plot_bounds(self, plot):
        """获取地块边界"""
        try:
            geom = shape(plot['geometry'])
            bounds = geom.bounds  # (minx, miny, maxx, maxy)
            return bounds
        except Exception as e:
            logger.error(f"获取地块边界失败: {str(e)}")
            # 返回默认边界
            return [116.4, 39.9, 116.43, 39.93]